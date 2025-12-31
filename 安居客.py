import csv
import re
from lxml import etree
import requests
import parsel
import pymysql
def start_url(page):
    url = f"https://bj.zu.anjuke.com/fangyuan/p{page}/"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "cookie": "SECKEY_ABVK=q5z6aBkbT2EXFoltBcpb34eIh2pq1ZpqzywGadW7g80%3D; BMAP_SECKEY=q5z6aBkbT2EXFoltBcpb31zEN3HiEIde34UiUcf0twzYetbI-rGalO8q80MOIUDRye2G-SQyxst4V088tIABqVwxzUUJhuYhpel8qF7CFfWk0iipGuroN-fTqeY4mYmm73i3O1t8Cy2rXwCPR-B5emJbvboUvmls8raZEifw5XpL41d9TVkR5NbLwq0gjvqqiTn5Pd7KVLQSEU1vMbXuLQ; sessid=A4340022-FA6F-44EF-BB16-A518A7D3FB8B; aQQ_ajkguid=7AB7FB94-3FFB-9FB9-1863-CCABF3C83750; twe=2; ajk-appVersion=; seo_source_type=1; fzq_h=c5616e17bb96195aad75274014079eb4_1764678555194_53c32acc97c44e4693a4e4f3840e6056_3085597564; obtain_by=2; id58=CrIqZ2ku26idf7AOBFkTAg==; xxzlclientid=ed25163b-04f7-454b-9a74-1764678573643; xxzlxxid=pfmxrkgdlc+ItiyuJbeI5gpJC8i4WYPzduHoA2A1zAqToiV2goYfzU107RalrpBZ6n3+; ctid=14; lps=https%3A%2F%2Fbj.zu.anjuke.com%2Ffangyuan%2F%7C; cmctid=1; wmda_visited_projects=%3B6289197098934; wmda_uuid=9733409db231c5174b0c81b5bd2df4a0; wmda_new_uuid=1; wmda_session_id_6289197098934=1764941555366-38089299-f2b4-5158; xxzlbbid=pfmbRPLsWWyIV0OSZwDv2PN/G6lNADSYY4qzp6l/NBOGL8czKZ8s1c6b2K41VUKaYZ9vSI727Lkxj8PIeiVpVgH6ldDYe0WFulstUJ2dEzZ16Y/j8j7/syHgoSjF0DaqaRZjNko4BFsxNzY0OTQxNjI3NzUyODY2_1"
    }

    response = requests.get(url,headers=headers)

    #print(response.text)

    html_text = response.text
    return html_text
""" re正则
def re_extract(html_text):
    #提取标题
    title_match = re.search(r'<b class="strongbox">(.*?)</b>',html_text)
    title = title_match.group(1) if title_match else ""
    #提取价格
    price_match = re.search(r'<strong class="price">(\d+)</strong>',html_text)
    price = price_match.group(1) if price_match else ""
    #提取户型
    house_type_match = re.search(r'<b.*?>(\d+)</b>室.*?<b.*?>(\d+)</b>厅', html_text)
    house_type = f'{house_type_match.group(1)}室{house_type_match.group(2)}厅' if house_type_match else ""
    #提取面积
    area_match = re.search(r'<b.*?>(\d+)</b>平米.*?', html_text)
    area = f"{area_match.group(1)}平米" if area_match else ""
    # 提取楼层                                  (?:<|</p>) 匹配一个左尖括号 < 或者匹配</p>结束标签 但不捕获这个匹配
    floor_match = re.search(r'平米<span>\|</span>(.*?)(?:<|</p>)', html_text)
    floor = floor_match.group(1).strip() if floor_match else ""
    #提取小区名字
    community_match = re.search(r'<address.*?>\s*<a.*?>(.*?)</a>', html_text)
    community = community_match.group(1).strip() if community_match else ""
    #提取区域、商圈、街道
    address_match = re.search(r'</a>&nbsp;&nbsp;\s*(.*?)<span.*?>-</span>(.*?)<span.*?>-</span>(.*?)</address>', html_text)
    if address_match:
        region = address_match.group(1).strip()
        business_district = address_match.group(2).strip()
        street = address_match.group(3).strip()
    else:
        region = business_district = street =""

    #提取标签
    tags_match = re.search(r'<p class="details-item bot-tag">(.*?)</p>',html_text,re.DOTALL)
    if tags_match:
        tags_section = tags_match.group(1).strip()
        tags = re.findall('<span class="cls-common">(.*?)</span>',tags_section)
        tags = ' '.join(tags)
    else:
        tags= ""



    dit = {
        '标题':title,
        '价格':price,
        '户型':house_type,
        '面积':area,
        "楼层":floor,
        '小区':community,
        '区域':region,
        '商圈':business_district,
        '街道':street,
        '标签':tags
    }



    print(dit)

"""
"""
def xpath_extract(html_text):
    html = etree.HTML(html_text)
    #提取所有房源div节点
    house_blocks = html.xpath('//div[@class="zu-itemmod clearfix"]')
    print(f"找到{len(house_blocks)}个房源")
    for house in house_blocks:
        #提取标题
        title = house.xpath('.//b[@class="strongbox"]/text()')
        title = title[0] if title else ""
        #提取价格
        price = house.xpath('.//strong[@class="price"]/text()')
        price = title[0] if title else ""
        #提取户型
        room_num = house.xpath('.//p[@class="details-item tag"]/b[@class="strongbox"][1]/text()')
        hall_num = house.xpath('.//p[@class="details-item tag"]/b[@class="strongbox"][2]/text()')
        house_type = f"{room_num[0]}室{hall_num[0]}厅" if room_num and hall_num else ""
        #提取面积
        area = house.xpath('.//p[@class="details-item tag"]/b[@class="strongbox"][3]/text()')
        area = f"{area[0]}平米" if area else ""
        # 提取楼层
        floor = house.xpath('.//p[@class="details-item tag"]/text()[contains(.,"层")]')
        floor = floor[0].strip() if floor else ""
        #提取小区名字
        community = house.xpath('.//address/a/text()')
        community = community[0].strip() if community else ""
        #提取区域、商圈、街道
        address_parts = house.xpath('.//address/text()')
        if len(address_parts) >= 3:
            region = address_parts[1].strip()
            business_district = address_parts[2].strip()
            street = address_parts[3].strip()
        else:
            region = business_district = street = ""


        # 提取标签
        tags = house.xpath('.//p[@class="details-item bot-tag"]/span[@class="cls-common"]/text()')
        tags = " ".join(tags) if tags else ""
        dit = {
                '标题':title,
                '价格':price,
                '户型':house_type,
                '面积':area,
                "楼层":floor,
                '小区':community,
                '区域':region,
                '商圈':business_district,
                '街道':street,
                '标签':tags
            }


        print(dit)
"""

def parsel_extract(html_text):
    selector = parsel.Selector(html_text)
    house_blocks = selector.css('.maincontent .list-content .zu-itemmod')
    #print(f"找到{len(house_blocks)}个房源")

    results = []

    for house in house_blocks:
        # 提取标题
        title = house.css('b.strongbox::text').get()
        # 提取价格
        price = house.css('strong.price::text').get()
        #提取户型
        info = house.css('p.details-item::text').getall()
        info_1 = house.css('p.details-item .strongbox::text').getall()
        info_2 = info[1:4] # 做切片的目的 是因为拿到 室 厅 平米 文字
        #print(info_1)
        #print(info_2)
        house_info = "".join([ j + i for i,j in zip(info_2,info_1)])
        house_type = house_info[:4]


        #提取面积
        area = house_info[4:]

        # 提取楼层
        floor = info[4].strip()

        #提取小区名字
        community_elem = house.css('address.details-item a::text').get()
        community = community_elem.strip() if community_elem else ""

        #提取区域、商圈、街道
        area_info = house.css('address.details-item::text').getall()
        region = area_info[1].strip()
        business_district = area_info[2].strip()
        street = area_info[3].strip()

        # 提取标签
        tags = ' '.join(house.css('p.bot-tag span::text').getall())


        dit = {
             '标题': title,
             '价格': price,
             '户型': house_type,
             '面积': area,
             "楼层": floor,
             '小区': community,
             '区域': region,
             '商圈': business_district,
             '街道': street,
             '标签': tags
        }
        results.append(dit)
        print(dit)
    return results


def save_to_database(house_data_list):
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123456',
        'database': 'anjuke_house'

    }
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        print("数据库连接成功")

        insert_sql = """
                INSERT INTO house (title, price, floor, house_type, area, community, region, business_district, street, tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cleaned_data = []
        for house_data in house_data_list:
            # 价格处理：提取数字
            price = house_data['价格']
            if price:
                price_match = re.search(r'(\d+)', str(price))
                price = float(price_match.group(1)) if price_match else 0.0
            else:
                price = 0.0
            # 面积处理：提取数字
            area = house_data['面积']
            if area:
                area_match = re.search(r'(\d+\.?\d*)', str(area))
                area = float(area_match.group(1)) if area_match else 0.0
            else:
                area = 0.0

                # 确保所有字段都有值
                title = house_data['标题'] or ""
                floor = house_data['楼层'] or ""
                house_type = house_data['户型'] or ""
                community = house_data['小区'] or ""


                region = house_data['区域'] or ""
                business_district = house_data['商圈'] or ""
                street = house_data['街道'] or ""
                tags = house_data['标签'] or ""
                cleaned_data.append((
                    title, price, floor, house_type, area,
                    community, region, business_district, street, tags
                ))
                # 执行批量插入
            cursor.executemany(insert_sql, cleaned_data)
            connection.commit()
            print(f"成功插入 {len(house_data_list)} 条数据到数据库")
            # 关闭连接
            cursor.close()
            connection.close()
            print("数据库连接已关闭")
            return True
    except Exception as e:
        print(f"数据库操作失败: {e}")
        return False



def main():


    #xpath_extract(html_text)

    f = open("anjuke_house.csv",mode='w',encoding='utf-8',newline='')
    csv_writer = csv.DictWriter(f,fieldnames=[
        '标题',
        '价格',
        '户型',
        '面积',
        "楼层",
        '小区',
        '区域',
        '商圈',
        '街道',
        '标签'
    ])
    csv_writer.writeheader()

    all_results = []

    for page in range(1,6):
        print(f"正在爬取第{page}")
        html_text = start_url(page)

        parsel_results = parsel_extract(html_text)
        #将当前页面的结果添加到总结果中
        all_results.extend(parsel_results)
        #将当前页面的输入csv
        csv_writer.writerows(parsel_results)
        print(f"第{page}页已写入CSV中")
    f.close()
    print(f"数据提取完成 共爬取{len(all_results)}条记录")
    if all_results:
        print("正在保存数据到数据库。。。")
        save_to_database(all_results)
    else:
        print("未获取到数据，跳过数据库保存")



"""    re正则
# 使用正则表达式 找到所有房源的div块                                                     re.DOTALL 匹配所有除了换行符（\n）之外的任何字符
    house_blocks = re.findall(r'<div class="zu-itemmod clearfix".*?/div>\s*</div>', html_text, re.DOTALL)
    print(f"找到{len(house_blocks)}个房源")

    #对每个房源应用提取
    #re_extract(html_text)
    for house in house_blocks:
        result = re_extract(house)
        
"""






if __name__ == "__main__":
    main()






































