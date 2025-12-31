# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiItem(scrapy.Item):
    # define the fields for your item here like:
    # 名字
    name = scrapy.Field()
    # 所属部分
    productName = scrapy.Field()
    # 职位描述
    description = scrapy.Field()
    # 招聘人数
    recruitNum = scrapy.Field()
    # 学历要求
    reqEducationName = scrapy.Field()
    # 工作经验要求
    reqWorkYearsName = scrapy.Field()
    # 职位要求
    requirement = scrapy.Field()
    #职位分类
    firstPostTypeName = scrapy.Field()
    # 工作地点
    workPlaceNameList = scrapy.Field()
    #下面2个变量主要是为了做通用的数据库表写入程序用的
    table_name = scrapy.Field() #表名
    table_files = scrapy.Field() #字段
