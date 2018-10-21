# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class HhSpider(scrapy.spiders.CrawlSpider):
    name = 'hh'
    download_delay = 2
    cookies = {'JSESSIONID': 'ABAAABAAAGFABEFB6061F6EB0EDC820F201E8DF3F9C2D42', ' Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1540116539', ' _ga': 'GA1.2.2067654053.1540116539', ' _gid': 'GA1.2.1796252207.1540116539', ' user_trace_token': '20181021180859-541f8462-d519-11e8-803a-5254005c3644', ' LGSID': '20181021180859-541f8762-d519-11e8-803a-5254005c3644', ' LGUID': '20181021180859-541f8a30-d519-11e8-803a-5254005c3644', ' X_HTTP_TOKEN': '682c6b1a994fd988d71872f8b6ce7a30', ' sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22166961970f24d0-0553ad5b2951d1-9393265-2073600-166961970f3726%22%2C%22%24device_id%22%3A%22166961970f24d0-0553ad5b2951d1-9393265-2073600-166961970f3726%22%7D', ' sajssdk_2015_cross_new_user': '1', ' LG_LOGIN_USER_ID': 'f685699c4540f607679698e6945edef8db7a07241f853399604c7c1d42a63abb', ' _putrc': '5788C16222BE03F2123F89F2B170EADC', ' login': 'true', ' unick': '%E9%99%88%E5%87%AF%E7%80%9A', ' showExpriedIndex': '1', ' showExpriedCompanyHome': '1', ' showExpriedMyPublish': '1', ' hasDeliver': '1', ' gate_login_token': 'fe0afbbe9b21c4356aef3ca5e5c3d212872dfd76f95d9c07f06ced78ccebabe7', ' index_location_city': '%E5%B9%BF%E5%B7%9E', ' TG-TRACK-CODE': 'index_checkmore', ' _gat': '1', ' LGRID': '20181021184402-396b1264-d51e-11e8-9552-525400f775ce', ' Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1540118642'}

    start_urls = [
        "https://www.lagou.com/gongsi/0-0-0-0?sortField=0#filterBox"
    ]
    link = LinkExtractor(restrict_xpaths=("//a[@class='bottom-item bottom-2 fl']"))
    rules = [
        Rule(link,
            callback='parse_item',
            follow=True
        )
    ]
    def start_requests(self):
        yield scrapy.Request(url = "https://www.lagou.com/",cookies=self.cookies)
    def parse_item(self, response):
        yield {
            'job_label' : 1,
            'company_name' : response.xpath("//div[@class='company_main']/h1/a/text()").re_first("\w+"),
            'logo' : 1,
            'about' : 1
        }
