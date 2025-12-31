import json
import random
import time

import scrapy

from ..items import WangyiItem


class JobSpider(scrapy.Spider):
    name = "job" #爬虫唯一标识 启动命令中使用
    allowed_domains = ["163.com"] # 允许爬取的域名
    start_urls = ["https://hr.163.com/api/hr163/position/queryPage"] # 起始URL

    headers = {
      'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
      'content-type':'application/json;charset=UTF-8',
      'referer':'https://hr.163.com/job-list.html'
    }

    #初始化数据库表结构信息
    def __init__(self):
        #数据库表名
        self.table_name = 'wangyijob'
        self.table_files = ['name','productName','description','recruitNum',
                            'reqEducationName','reqWorkYearsName','requirement',
                            'firstPostTypeName','workPlaceNameList']

    #重写起始的请求
    # start_requests 方法必须返回一个包含request对象的可迭代对象（比如列表或者生成器）
    def start_requests(self):
        #初始页数和每页条数
        current_page = 1
        page_size = 10


        payload = {
            "currentPage": current_page, #起始页
            "pageSize": page_size, # 每页显示的条数
            "keyword": "python" #搜索关键词
        }
        #生成request对象
        yield scrapy.Request(
            url = self.start_urls[0],
            method ="POST", #必须使用POST方法
            headers = self.headers,
            body = json.dumps(payload), #序列化json参数
            callback=self.parse, #指定响应处理函数
            #传递元数据
            meta = {
                "current_page":current_page,
                "page_size": page_size
            }
        )


    #处理返回的结果
    def parse(self, response):
        dic = response.json()
        #提取职位列表数据
        job_list = dic['data']['list']

        for job in job_list:
            #必须每个循环创建Item对象（防止数据覆盖）
            item = WangyiItem()
            #填充数据库表结构信息
            item['table_name'] =self.table_name
            item['table_files'] = self.table_files

            #名字
            item['name']=job['name']
            #所属部分
            item['productName']=job['productName']
            #职位描述
            item['description'] = job['description'].replace('\t','').replace('\n','')
            #招聘人数
            item['recruitNum'] = job['recruitNum']
            #学历要求
            item['reqEducationName'] = job['productName']
            # 工作经验要求
            item['reqWorkYearsName'] = job['reqWorkYearsName']
            #职位要求
            item['requirement'] = job['requirement'].replace('\t','').replace('\n','')
            # 职位分类
            item['firstPostTypeName'] = job['firstPostTypeName']
            # 工作地点
            item['workPlaceNameList'] = str(job['workPlaceNameList']).replace('[','').replace(']','').replace("'",'')

            #处理数据
            yield item

        #获取总页数和总职位数
        total_positions = dic['data']['total']
        total_pages = dic['data']['pages']
        self.logger.info(f"总分页数: {total_pages},总数据: {total_positions}")

        #模拟翻页
        #判断是否还有下一页
        current_page = response.meta['current_page']
        page_size = response.meta['page_size']
        if current_page < total_pages:
            #随机延迟1-3秒
            delay = random.uniform(1,3)
            self.logger.info(f"随机延迟设置：等待{delay:.2f} 秒后继续下一页请求")
            #时间同步阻塞
            time.sleep(delay)


            #计算下一页页码
            next_page = current_page +1

            payload = {
                "currentPage": next_page,  # 起始页
                "pageSize": page_size,  # 每页显示的条数
                "keyword": "python"  # 搜索关键词
            }
            # 生成request对象
            yield scrapy.Request(
                url=self.start_urls[0],
                method="POST",  # 必须使用POST方法
                headers=self.headers,
                body=json.dumps(payload),  # 序列化json参数
                callback=self.parse,  # 指定响应处理函数
                # 传递元数据
                meta={
                    "current_page": next_page,
                    "page_size": page_size
                }
            )
        else:
            self.logger.info("爬虫任务完成！ 已到达最后一页")