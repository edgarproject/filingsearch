# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from .src.utils.items import GetedgarItem
import json
class GetedgarPipeline(object):

    def __int__(self):
        #self.file = open('items.jl','wb')
        pass

    def process_item(self, item, spider):
        
        #if item['Finish'] < 7:
           # item = GetedgarItem()
            #item['Company'] = "Repeat"
        #line = json.dump(dict(item)) + "\n"
        #self.file.write(line)
        print ("---------------------------------------------------")
        print (item['Company'])
        print ("---------------------------------------------------")
        return item