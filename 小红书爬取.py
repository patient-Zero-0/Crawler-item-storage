import os.path
import random
import re
from time import sleep
import csv

import requests
from DrissionPage import ChromiumPage


if not os.path.exists('xhs'):
    os.makedirs('xhs')

#创建CSV
csv_path = 'xhs/xhs.csv'
if not os.path.exists(csv_path):
    with open(csv_path,'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        #设置表头
        writer.writerow(['note_id','title','url','image_count','status','error_info'])

value = input("请输入想要爬取的数据:")

#创建浏览器实例
page = ChromiumPage()

tab = page.latest_tab

#开始监听网络数据包
tab.listen.start('web/v1/search/notes')

tab.get(f'https://www.xiaohongshu.com/search_result/?keyword={value}&type=51')

#等待并且获取
r = tab.listen.wait()

json_data = r.response.body


#初始化列表用于存储所有抓取到的笔记项
all_item_dict = []




while json_data.get('data',{}).get('has_more',False):

    items = json_data['data']['items']
    print(f"当前加载的数据项:{len(items)}")
    #遍历当前页的所有笔记项
    for item in items:
        if item not in all_item_dict:
            all_item_dict.append(item)
            print(f"追加数据：ID={item['id']}")
        else:
            print(f"跳过重复的数据：ID={item['id']}")

    #滚动页面以触发加载更多内容
    tab.scroll.to_bottom()#滚到底部
    tab.run_js("window.scrollBy(0,2000)")#执行js额外滚动2000个像素
    tab.set.scroll.wait_complete()#等待滚动完成
    print('滑动到页面底部，等待加载更多内容...')
    sleep(random.uniform(2,4))
    r = tab.listen.wait()
    json_data = r.response.body#更新js数据
    print(f'总加载数据:{len(all_item_dict)}')


#遍历所有抓到的笔记项
for item in all_item_dict:
    if item['model_type'] != 'note':
        continue

    try:
        note_id = item['id']#笔记ID
        token_ = item['xsec_token']  # 笔记ID
        #构建完整的url地址
        url = f'https://www.xiaohongshu.com/explore/{note_id}?xsec_token={token_}&xsec_source=pc_search&source=unknown'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            'referer': 'https://www.xiaohongshu.com/'
        }

        response = requests.get(url,headers=headers,timeout=10)

        html = response.text
        #使用正则匹配标题
        old_title = re.findall('<meta name="og:title" content="(.*?)">',html)[0]
        #过滤非法字符
        title = re.sub(r'[\\/*?:"<>|]', '', old_title)
        title = title[:50]
        print(f'标题：{title}')

        #图片链接
        image_urls = re.findall('<meta name="og:image" content="(.*?)">',html)

        print(f"发现{len(image_urls)}张图片")

        #为当前笔记创建文件夹
        #格式：标题_笔记ID
        note_folder = os.path.join('xhs_data',f"{title}_{note_id}")
        if not os.path.exists(note_folder):
            os.makedirs(note_folder)

        #下载图片
        #enumerate 遍历所有图片链接 并获取索引
        img_count = 0#下载图片的计数器

        for i,image_url in enumerate(image_urls):
            try:
                print(f"图片链接：{image_url}")

                img_content = requests.get(image_url,timeout=10).content

                img_path = os.path.join(note_folder,f'image_{i+1}.jpg')

                #图片保存到本地
                with open(img_path,'wb') as f:
                    f.write(img_content)
                img_count += 1
                print(f"已保存图片{i + 1}/{len(image_urls)}")                #暂停 避免下载过快
                sleep(0.5)
            except Exception as e:
                print(e)

        with open(csv_path,'a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)

            writer.writerow([note_id,title,url,img_count,'ok',''])

        print(f"成功保存图片:{title},共{img_count}张")
    except Exception as e:
        print(f"处理笔记{note_id}时错误：{e}")
        with open(csv_path,'a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)

            writer.writerow([note_id,'',url,0,'err',str(e)])


print("数据采集完成")
sleep(3)
tab.clear_cache(cookies=False)#清理浏览器缓存（保留cookies）


