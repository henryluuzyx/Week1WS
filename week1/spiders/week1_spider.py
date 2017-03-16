# -*- coding: utf-8 -*-
import scrapy
import os
import time

class Week1Spider(scrapy.Spider):
    name = 'week1'
    domains = 'http://www.baomoi.com'
    allowed_domains = ['baomoi.com', 'tuoitre.vn']
    page_count = 0
    data_directory = 'data'
    downloadkps = 0
    timepass = 0
    try:
        os.makedirs(data_directory)
    except Exception:
        pass

    def start_requests(self):
        yield scrapy.Request('http://www.baomoi.com/', self.parse_baomoi)
        yield scrapy.Request('http://tuoitre.vn/', self.parse_baomoi)

    def parse_baomoi(self, response):
        # self.page_count += 1
        # # Write HTML content to a file
        # with open(os.path.join(self.data_directory, str(self.page_count)), 'wb') as f:
        #     print>>f, response.body
        # # A file contains URLs of all visited pages
        # with open(os.path.join(self.data_directory, 'downloadList.txt'), 'ab') as f:
        #     print>>f, response.url
        #find next
    	next_page = scrapy.Selector(response).xpath('//a/@href').extract()
        for next in next_page:
        	#for baomoi
            if(next.startswith("/") & next.endswith("epi")):
                yield scrapy.Request(self.domains + next,
                    callback=self.parse_save,
                    meta={'start_time': time.time()});
            if(next.startswith("http://")):
            	yield scrapy.Request(next,
                    callback=self.parse_save,
                    meta={'start_time': time.time()});


    def parse_save(self, response):
    	self.page_count += 1
        self.timepass += time.time()-response.meta['start_time']
        self.downloadkps += len(response.body)
        print self.timepass
        # download_size= int(response.headers['Content-Length'])
        # print download_size
        print self.downloadkps
        # print self.page_count
        print self.downloadkps/(1024*self.timepass*self.page_count)
        # Write HTML content to a file
        with open(os.path.join(self.data_directory, str(self.page_count)), 'wb') as f:
            print>>f, response.body
        # A file contains URLs of all visited pages
        with open(os.path.join(self.data_directory, 'downloadList.txt'), 'ab') as f:
            print>>f, response.url