# -*- coding: utf-8 -*-
import scrapy
from Koolearn.items import KoolearnItem

class KoolearnSpider(scrapy.Spider):
    name = 'koolearn'
    # allowed_domains = ['']
    start_urls = ['http://flow.koolearn.com/shiti/list-1-1-0-1.html?yyue=a21bo.50862.201879']

    base_url = "http://flow.koolearn.com"
    end_url = "?yyue=a21bo.50862.201879"

    def parse(self, response):

        # 处理500
        if response.status == 500:
            itemNum = self.txt_wrap_by('-', '.', response.url)[6:10]
            new_itemNum_url = 'http://flow.koolearn.com/shiti/list-1-1-0-' + itemNum + '.html?yyue=a21bo.50862.201879'
            yield scrapy.Request(new_itemNum_url, self.parse)


        # 年级
        # Item['grade'] = response.xpath("//div[@class='filter-item g-clear'][1]//li[@class='active']/a/text())").extract()[0]
        
        # 科目
        # Item['subject'] = response.xpath("//div[@class='filter-item g-clear'][2]//li[@class='active']/a/text()").extract()[0]

        # 问题查看答案列表链接
        watch_answer_urls = response.xpath("//a[text()='查看答案']/@href").extract()
        
        for url in watch_answer_urls:
            answer_url = self.base_url + url + self.end_url
            yield scrapy.Request(answer_url, self.answer_parse)

        # 下一页
        if len( response.xpath("//a[@class='next']/@href")):
            next_url = self.base_url + response.xpath("//a[@class='next']/@href").extract()[0]
            yield scrapy.Request(next_url, self.parse)
        
        return

    def answer_parse(self, response):
        item = KoolearnItem()
        
        # xpath解析response
        if len(response.xpath("/html/body/div[1]/div[2]/div[1]/a[1]/text()")) == 0:
            item['sourse'] = ""
        item['sourse'] = response.xpath("/html/body/div[1]/div[2]/div[1]/a[1]/text()").extract()[0]
        
        if len(response.xpath("/html/body/div[1]/div[2]/div[1]/a[2]/text()"))  == 0:
            item['grade'] = ""
        item['grade'] = response.xpath("/html/body/div[1]/div[2]/div[1]/a[2]/text()").extract()[0][0:2]
        
        if len(response.xpath("/html/body/div[1]/div[2]/div[1]/a[2]/text()"))  == 0:
            item['subject'] = ""
        item['subject'] = response.xpath("/html/body/div[1]/div[2]/div[1]/a[2]/text()").extract()[0][2:4]
        
        if len(response.xpath("/html/body/div[1]/div[2]/div[1]/a[2]/text()"))  == 0:
            item['s_type'] = ""
        item['s_type'] = response.xpath("/html/body/div[1]/div[2]/div[1]/a[2]/text()").extract()[0][4:6]
        
        if len(response.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/label[1]/span[2]/text()")) == 0:
            item['question_num'] = ""
        item['question_num'] = response.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/label[1]/span[2]/text()").extract()[0]

        if len(response.xpath("/html/body/div[1]/div[2]/div[1]/a[3]/text()"))  == 0:
            item['question_type'] = ""
        item['question_type'] = response.xpath("/html/body/div[1]/div[2]/div[1]/a[3]/text()").extract()[0]

        if len(response.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/label[2]/span[2]/text()")) == 0:
            item['difficulty_level'] = ""
        item['difficulty_level'] = response.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/label[2]/span[2]/text()").extract()[0]

        if len(response.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/text()")) == 0:
            item['question_item'] = ""
        item['question_value'] = response.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/text()").extract()

        if len(response.xpath("//*[@id='i-tab-content']/div/text()")) == 0:
            item['answer_value'] = ""
        item['answer_value'] = response.xpath("//*[@id='i-tab-content']/div/text()").extract()[0]
        
        if len(response.xpath("//*[@id='i-tab-content1']/div/text()")): 
            if len(response.xpath("/html/body/div[1]/div[2]/div[2]/div[4]/div[2]/a[2]/@href")) == 0:
                 item['answer_extend_link'] = ""
            item['answer_extend_link'] = self.base_url + response.xpath("/html/body/div[1]/div[2]/div[2]/div[4]/div[2]/a[2]/@href").extract()[0] + self.end_url
            item['answer_explain'] = response.xpath("//*[@id='i-tab-content1']/div/text()").extract()[0]
        else:
            if len(response.xpath("/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/a[2]/@href")) == 0:
                 item['answer_extend_link'] = ""
            item['answer_extend_link'] = self.base_url + response.xpath("/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/a[2]/@href").extract()[0] + self.end_url
            item['answer_explain'] = ""
        
        # print(item)
        yield item



    #取字符串中两个符号之间
    def txt_wrap_by(self,start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()   
