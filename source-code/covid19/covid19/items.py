# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# url list
class Covid19ListItem(scrapy.Item):
    date = scrapy.Field()
    href = scrapy.Field()
    
# article contents
class Covid19TextItem(scrapy.Item):
    href = scrapy.Field()
    text = scrapy.Field()