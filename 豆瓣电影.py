import re

import requests
from openpyxl import Workbook



def get_url():
    url_start = "https://movie.douban.com/top250?start={}&filter="
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    wb = Workbook()

    ws = wb.active

    ws.append(['电影名称','经典台词'])


    for i in range(0,10):
        start = i * 25
        url = url_start.format(start)
        print(f"正在抓取{i+1}页 {url}")
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            parse_data_with_regex(response.text,ws)
        except Exception as e:
            print(f"抓{i+1}页失败：{e}")
    wb.save("豆瓣9.4以上高分电影.xlsx")
    print("数据保存完毕")


def parse_data_with_regex(html_content,ws):
   # item_pattern = re.compile('<div class="item">.*?<span class="title">(.*?)</span>.*?<span class="rating_num" property="v:average">(.*?)</span>.*?<span>(.*?)</span></p>.*?',re.S)

    #print(html_content)

   item_pattern = re.compile(
       r'<div class="item">.*?<span class="title">(.*?)</span>.*?'  # 电影名称
       r'<span class="rating_num".*?>(.*?)</span>.*?'  # 评分
       r'(?:(<p class="quote">.*?<span>(.*?)</span>.*?</p>)|(?=<div class="item">))',  # 经典台词（可选）
       re.S
   )

   items = item_pattern.findall(html_content)

   for item in items:
       try:
           name = item[0].strip()
           rating = float(item[1].strip())
           if rating < 9.5 :
               continue


           quote = item[3].strip() if item[3] else "暂无台词"

           ws.append([name,quote])
           print(f"已保存：{name} | 评分：{rating} | 台词：{quote}")
       except Exception as e:
           print(f"解析电影信息时出错：{e}")









if __name__ == '__main__':
    get_url()
