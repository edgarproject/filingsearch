# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
import scrapy
import urllib
import re
from ..src.utils.read_json import ReadJson
from ..src.utils.items import GetedgarItem
from ..src.response.log import *
from ..src.response.save_file import SaveFile
from ..src.response.pdf import *


class GetEdgarSpider(CrawlSpider):
    name = "search"
    allowed_domains = ["sec.gov"]
    cont = 1
    numero = 0
    #def __int__(self,sic=None, *args, **kwargs):
        #super(GetEdgarSpider, self).__init__(*args, **kwargs)
    print_log("INITIATING PROJECT GETEDGAR")
    fileJson = ReadJson()
    SICs = fileJson.get_json_key("sics")
    print_log("READS THE SELECTED SICS")
    urls = []
    if fileJson.get_json_key("company_specifies")["active"] is False:
        for sic in SICs:
            urls.append('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC='+str(sic)+'&owner=include&match=&start=00&count=100&hidefilings=0')
        start_urls = urls
    else:
        for CIK in fileJson.get_json_key("company_specifies")["companies_CIKs"]:
            urls.append('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type=&dateb=&owner=include&start=0&count=100'.format(str(CIK)))
        start_urls = urls
    print_log("SE CONSTRUYEN LAS URLS")
    keydocs = fileJson.get_json_key("key_docs")
    keywords = fileJson.get_json_key("keywords")
    keywords_false = fileJson.get_json_key("keywords_false")
    endFile = fileJson.get_json_key("search_depth_in_file")

    def parse(self, response):
        try:
            selector = Selector(response)
            companys = selector.xpath('//table[@class="tableFile2"]//tr')
            a = companys[0].xpath('th[1]//text()').extract()[0]
            can = 100
            if (str(a) == 'CIK'):
                for i in range(1,len(companys)):
                    item = GetedgarItem()
                    tr = companys[i]
                    self.numero = self.numero + 1
                    item['CIK'] = tr.xpath('td[1]/a/text()').extract()[0]
                    item['SIC'] = response.url[63:67]
                    item['Company'] = tr.xpath('td[2]/text()').extract()[0]
                    item['UrlAll'] = "www.sec.gov" + tr.xpath('td[1]/a/@href').extract()[0]
                    item['DocType'] = {}
                    item['UrlDoc_array'] = {}
                    item['Finish'] = 0
                    for j in range(0,len(self.keydocs)):
                        link = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+item['CIK']\
                                          +"&type="+str(self.keydocs[j])+"&dateb=&owner=exclude&count="+str(can)
                        item['UrlDoc_array'][j] = {'Link':link}
                        request = scrapy.Request(link,callback=self.parseGetFillings)
                        request.meta['item'] = item
                        request.meta['i'] = j
                        yield request
                    #Loads a new page with new companies
                    try:
                        next_companys = selector.xpath('//input[@value="Next 100"]/@onclick').extract()
                        if next_companys:
                            new_url = 'https://www.sec.gov'+str(next_companys[0])[17:-1] #Obtains the new url
                            new_request = scrapy.Request(new_url,callback=self.parse)
                            yield new_request
                        else:
                            pass
                    except:
                        pass
            else:
                if(str(a) == 'Filings'):
                    item = GetedgarItem()
                    item['CIK'] = response.xpath('//input[@name="CIK"]/@value').extract()[0]
                    item['SIC'] = response.xpath('//p[@class="identInfo"]/a/text()').extract()[0]
                    item['Company'] = response.xpath('//span[@class="companyName"]//text()').extract()[0]
                    item['DocType'] = {}
                    item['UrlDoc_array'] = {}
                    item['Finish'] = 0
                    for j in range(0,len(self.keydocs)):
                        link = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+item['CIK']\
                                          +"&type="+str(self.keydocs[j])+"&dateb=&owner=exclude&count="+str(can)
                        item['UrlDoc_array'][j] = {'Link':link}
                        request = scrapy.Request(link,callback=self.parseGetFillings)
                        request.meta['item'] = item
                        request.meta['i'] = j
                        yield request
        except IOError as e:
            print_log("I/O error({0}): {1}".format(e.errno, e.strerror))
            print_log('==========================Company no encontrada================================')


    def parseGetFillings(self, response):
        """
        Metodo para sacar los datos de la compañia con el filtro de KeyDocs
        :param response:
        :return: Fillinh, Fecha, Url donde se encuentran los docuemntos
        """
        item = response.meta['item']
        sel = Selector(response)
        next_companys = sel.xpath('//input[@value="Next 100"]/@onclick').extract()
        if next_companys:
            fillings = sel.xpath('//table[@class="tableFile2"]//tr')
            if len(fillings)>1:
                for j in range(1,len(fillings)):
                    tr = fillings[j]
                    fill = tr.xpath('td[1]/text()').extract()[0]
                    date = tr.xpath('td[4]/text()').extract()[0]
                    link = "https://www.sec.gov"+tr.xpath('td[2]/a/@href').extract()[0]
                    request = scrapy.Request(link, callback=self.parseGetDetailsDocs)
                    request.meta['item'] = item
                    request.meta['i'] = j
                    request.meta['Date_doc'] = date
                    yield request
            else:
                print_log("-----------------Sin datos---------------------------------")
            new_url = 'https://www.sec.gov'+str(next_companys[0])[17:-1] #obtains the new url
            new_request = scrapy.Request(new_url,callback=self.parseGetFillings)
            new_request.meta['item'] = item
            yield new_request
        else:
            fillings = sel.xpath('//table[@class="tableFile2"]//tr')
            if len(fillings)>1:
                for j in range(1,len(fillings)):
                    tr = fillings[j]
                    fill = tr.xpath('td[1]/text()').extract()[0]
                    date = tr.xpath('td[4]/text()').extract()[0]
                    link = "https://www.sec.gov"+tr.xpath('td[2]/a/@href').extract()[0]
                    request = scrapy.Request(link, callback=self.parseGetDetailsDocs)
                    request.meta['item'] = item
                    request.meta['i'] = j
                    request.meta['Date_doc'] = date
                    yield request
            else:
                print_log("-----------------Sin datos---------------------------------")
        yield item


    def parseGetDetailsDocs(self,response):
        item = response.meta['item']
        i = response.meta['i']
        date_doc = response.meta['Date_doc']
        sel = Selector(response)
        dates = sel.xpath('//table[@summary="Document Format Files"]//tr')
        find = False
        if len(dates) > 1:
            for k in range(1,len(dates)):
                try:
                    nameDoc = dates[k].xpath('td[3]/a/text()').extract()[0]
                    descriptionDoc = dates[k].xpath('td[2]/text()').extract()[0]
                except:
                    nameDoc = "nullo.gif"
                    descriptionDoc = "nullo"
                extencions = ['htm','html','txt']
                if nameDoc[-3:] in extencions:
                    urlDoc = "https://www.sec.gov"+dates[k].xpath('td[3]/a/@href').extract()[0]
                    arr_details = [item['Company'],item['CIK'],nameDoc,descriptionDoc,urlDoc,item['SIC'],response.url,date_doc]
                    if not self.falsePositive(descriptionDoc.lower()):
                        if self.searchWords(descriptionDoc.lower()):
                            item['Doc'] = [nameDoc,urlDoc,descriptionDoc,response.url]
                            SaveFile.write_in_doc(urlDoc, nameDoc[:-4], descriptionDoc, item['Company'], item['CIK'],
                                                  item['SIC'], response.url, date_doc,
                                                  self.fileJson.get_json_key("file_out")["name"])
                            if self.fileJson.get_json_key("response_pdf")["active"] is True:
                                create_pdf(urlDoc,nameDoc[:-4])
                        else:
                            request = scrapy.Request(arr_details[4],callback=self.searchInDoc)
                            request.meta['Dates'] = arr_details
                            yield request
                    else:
                        pass
        yield item

    def searchInDoc(self,response):
        sel = Selector(response)
        date = response.meta['Dates']
        #text = ''.join(sel.xpath('//font/text()').extract()[0:15])
        text = ''.join(sel.xpath('//text()').extract()[0:int(self.endFile)])
        text = text.lower()
        for key in self.keywords:
            if key in text:
                SaveFile.write_in_doc(response.url, date[2][:-4], date[3], date[0], date[1], date[5], date[6], date[7],
                                      self.fileJson.get_json_key("file_out")["name"])
                if self.fileJson.get_json_key("response_pdf")["active"] is True:
                    create_pdf(response.url, date[2][:-4])
                return True
    #======================================================================
    #   Method for searching the keywords in the titles of the tables
    #======================================================================

    def searchWords(self, line):
        for i in self.keywords:
            if i in line:
                return True
        return False

    def falsePositive(self, line):
        for i in self.keywords_false:
            if i in line:
                return True
        return False
