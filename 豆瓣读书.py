import requests
import os
import re

for i in range(1,3):
    url = f"https://book.douban.com/latest?subcat=%E5%85%A8%E9%83%A8&p={i}&updated_at="
    print(f"正在获取第{i}页",url)

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }


    response = requests.get(url,headers=headers)


    html_data = response.text

    result = re.findall('<li\sclass="media\sclearfix.*?align="left"\ssrc="(.*?)"/>.*?<div\sclass="media__body.*?href="(.*?)">(.*?)</a>.*?<p\sclass="subject-abstract\scolor-gray">(.*?)</p>',html_data,re.S)



    for i in result:
        photo = i[0]
        title_link = i[1]
        title = i[2]
        auth_datails = i[3].strip()

        print(photo)
        print(title_link)
        print(title)
        print(auth_datails)

        print("-" * 50 +"\n")

        with open("douban_data.txt","a",encoding="utf_8") as f:
            f.write(title + "\n")
            f.write(title_link + "\n")
            f.write(auth_datails + "\n")
            f.write(photo + "\n")
            f.write("-" * 50 +"\n")

        if not os.path.exists("douban_image"):
            os.mkdir("douban_image")
        img_data = requests.get(photo,headers=headers).content

        with open("douban_image/{}.jpg".format(title),"wb") as f:
            f.write(img_data)
