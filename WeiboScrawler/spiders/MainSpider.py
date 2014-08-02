# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.item import Item
from scrapy.selector import Selector
from scrapy.http import Request
from loginModule import LoginModule
import re
import os
import json
from render import Render


class BaseWeiboSpider(Spider):
    name='Test'
    allowed_domains=['weibo.com',]

    def __init__(self):
        print('BaseSpider')
        loginor=LoginModule()
        username='adoni1203@gmail.com'
        password='9261adoni'
        result=loginor.login(username,password)
        if(not result[0]):
            print('Error!')
        self.cookie=result[1]

    def simple_parse(self,response):
        f=open('a.html','w')
        f.write(response.body)
        f.close()
        r = Render(response.body)
        html = r.frame.toHtml()
        html=unicode(html,'utf-8','ignore').encode('utf-8')
        print(type(html))
        sel=Selector(text=html)
        all_news=sel.xpath('//div[@class="WB_feed WB_feed_self"]//div').extract()
        print(len(all_news))
        f=open('b.html','w')
        f.write(html)
        f.close()

    def start_requests(self):
        start_url='http://weibo.com/p/1005052337295450/weibo?from=page_100505_home&wvr=5.1&mod=weibomore#3507560357470567'
        yield Request(
                url=start_url,
                cookies=self.cookie,
                callback=self.simple_parse
            )
