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
        #sel=Selector(response)
        #all_news=sel.xpath('//div[@class="WB_feed"]//div').extract()
        #print(len(all_news))
        url = './a.html'
        r = Render(url)
        html = r.frame.toHtml().toUtf8()
        f=open('b.html','w')
        f.write(html)
        f.close()

    def start_requests(self):
        yield Request(url='http://weibo.com/u/3623327573/home?wvr=5',
            cookies=self.cookie,
            callback=self.simple_parse
            )
