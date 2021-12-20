# -*- coding: utf-8 -*-

from scrapy import Request, Spider
import sys
sys.path.append('../../covid19')
from covid19.items import Covid19ListItem


class Covid19ListSpider(Spider):
    """
    Collect the url list.
    """
    name = "covid19list"
    allowed_domains = ["nhc.gov.cn"]
    
    def start_requests(self):
        base_url = "http://www.nhc.gov.cn/xcs/yqtb/"
        for i in range(1, 31):
            if i == 1:
                url = base_url + "list_gzbd.shtml"
            else:
                url = base_url + "list_gzbd_{}.shtml".format(i)
            try:
                yield Request(url = url, callback = self.parse)
            except:
                break
                
    def parse(self, response):
        item = Covid19ListItem()
        base_url = r"http://www.nhc.gov.cn/"
        try:
            dates = response.xpath('//div[@class = "list"]//ul[@class = "zxxx_list"]//li//span/text()').extract()
            hrefs = response.xpath('//div[@class = "list"]//ul[@class = "zxxx_list"]//li//a/@href').extract()
            for i in range(len(dates)):
                item["date"] = dates[i]
                item["href"] = base_url + hrefs[i]
                yield item
        except:
            print(response.url)
            