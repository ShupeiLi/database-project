# -*- coding: utf-8 -*-

from scrapy import Request, Spider
import sys
sys.path.append('../../covid19')
from covid19.items import Covid19TextItem
import pandas as pd
from tqdm import tqdm


class Covid19ArticleSpider(Spider):
    """
    Collect the url list.
    """
    name = "covid19article"
    allowed_domains = ["nhc.gov.cn"]
    
    def start_requests(self):
        urlPath = r"D:\Document\大学资料\大四上课件\数据库与企业数据管理\项目\database-project\source-code\covid19\covid19list.csv"
        urlDf = pd.read_csv(urlPath)
        for i in tqdm(range(urlDf.shape[0])):
            url = urlDf.iloc[i, 1]
            yield Request(url = url, callback = self.parse)
                
    def parse(self, response):
        item = Covid19TextItem()
        try:
            item['href'] = response.url
            item['text'] = "".join(response.xpath('//div[@class = "con"]//p/text()').extract())
            yield item
        except:
            print(response.url)