# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

import pymysql
from itemadapter import ItemAdapter

"""
    同步插入数据库
"""
class WangyiPipeline:

    #在爬虫开启的时候仅执行一次
    def __init__(self):
        """初始化数据库连接"""
        self.connect = pymysql.connect(host='localhost',
                                       user='root',
                                       passwd='123456',
                                       db='wydb',
                                       charset='utf8',
                                       port=3306)
        #创建游标对象
        self.cursor = self.connect.cursor()

    """
        处理item的核心方法
         item 爬虫传递的数据项
         spider 触发该管道的爬虫实例
    """
    def process_item(self, item, spider):

        #从item中获取表结构信息
        table_name = item.get('table_name')
        table_files = item.get('table_files')
        #检验必要参数
        if table_files is None or table_name is None:
            raise Exception("必须要传入表名以及字段名 不能为空")

        #构建sql --------------------------------------------------
        # insert into 表名(字段名) values(%s,%s,%s,%s,%s,%s,%s,%s)

        values_params = ", ".join(['%s'] * len(table_files))
        #字段列表字符串 比如 "name,age,...."
        keys = ", ".join(table_files)
        #字段值
        values = ['%s' % str(item.get(i,'')) for i in table_files ]
        #动态生成sql
        insert_sql = f"INSERT INTO {table_name}({keys}) VALUES ({values_params})"
        try:
            #执行sql语句
            self.cursor.execute(insert_sql,tuple(values))
            logging.info("数据插入成功 => + 1")
        except Exception as e:
            logging.error("执行sql异常 => " + str(e))
            pass
        finally:
            #提交事务
            self.connect.commit()

        return item

    #爬虫关闭时自动调用 释放资源
    def close_spider(self):
        self.connect.close()
        self.cursor.close()