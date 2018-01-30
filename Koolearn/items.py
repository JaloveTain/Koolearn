# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoolearnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    sourse = scrapy.Field() # 题目来源
    grade = scrapy.Field() # 年级: 高中,初中
    subject = scrapy.Field() # 学科：语文,数学...
    s_type = scrapy.Field() # 试卷
    q_link = scrapy.Field() # 题目链接
    question_num = scrapy.Field() # 单选,多选
    question_type = scrapy.Field() # 题目类型
    difficulty_level = scrapy.Field() # 难度等级
    question_value = scrapy.Field() # 问题内容
    answer_value = scrapy.Field() # 问题答案
    answer_extend_link = scrapy.Field() # 问题拓展链接
    answer_explain = scrapy.Field() # 答案解析

    
