# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class GetedgarItem(Item):
    CIK = Field()
    SIC = Field()
    Company = Field()
    UrlAll = Field()
    Url10_k = Field()
    DocType = Field()

    #Companys
    UrlDoc_array = Field()
    Finish = Field()
    Doc = Field()