# -*- coding: utf-8 -*-

# Scrapy settings for getedgar project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'getedgar'
SPIDER_MODULES = ['getedgar.spiders']
NEWSPIDER_MODULE = 'getedgar.spiders'
ITEM_PIPELINES = {'getedgar.pipelines.GetedgarPipeline':1}
CONCURRENT_REQUESTS = 30 #Ajilisar la busqueda
#ROBOTSTXT_OBEY = True

