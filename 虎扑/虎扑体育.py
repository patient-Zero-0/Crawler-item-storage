import requests
import jsonpath
import json
import csv
import os.path
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=utf-8",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "smidV2": "2025122508325866f1e0278456e70eea35e09b9086626b001248bad515432d0"
}
url = "https://www.hupu.com/home/v1/news"

csv_path = '虎扑新闻数据.csv'


if not os.path.exists('虎扑新闻数据'):
    os.makedirs('虎扑新闻数据')

if not os.path.exists(csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 设置表头
        writer.writerow(['title', 'content', 'topicName', 'tid'])


for i in range(1,31):
    params = {
        "pageNo": i,
        "pageSize": "50"
    }

    response = requests.get(url, headers=headers, cookies=cookies, params=params).json()




    datas = response['data']
    for data in datas:
        title = data['title']
        content = data['content']
        topicName = data['topicName']
        tid = data['tid']
        #拼接新闻链接
        new_url = f"https://bbs.hupu.com/{tid}.html"
        all_news = [title, content, topicName, new_url]
        print(all_news)

        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(all_news)









































































