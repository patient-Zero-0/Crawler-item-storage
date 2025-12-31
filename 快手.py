import os.path
import re
import requests
import jsonpath
import json


url = "https://www.kuaishou.com/rest/v/profile/feed"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "cookie": "kpf=PC_WEB; clientid=3; did=web_c1127ff4e339b2a8060f0cac03bc4501; kwpsecproductname=kuaishou-vision; didv=1763892146000; userId=5127814235; kuaishou.server.webday7_st=ChprdWFpc2hvdS5zZXJ2ZXIud2ViZGF5Ny5zdBKwAawSmkPDUrn90_J9m8IBCknSzUnAR0hkbA431dSG_zcvhvcmMQYpyPr4-yiAhC6xml_uqtW3FLURokbi0qg9bMAPGNYAXRZplvIy4pStSb5BVL1TCg2uKBgIHdD8taL2HkWa9YeE4rlrxpN8Z7cltO2S10X07WRZ6f8s48kQYYEDWqC7ZV93SZ7VizA7bnlBKuCHlnu1q0ZJoxQmIlBCYadgPZys9c6zg52EiyzokLFvGhLnL33oyPAVhFFV1o7h2Db3JhgiIH7Lm7ywA0I7gDipsj082LF0gjV7nlgSFLwIgJdyimn_KAUwAQ; kuaishou.server.webday7_ph=e802d875961e9c91014d864e31933d6d917c; kwpsecproductname=kuaishou-vision; kwssectoken=nGNU6V0pIIsuO3r31wL2UVl4BXzgfiy81O69FD9euRvkzJoyI+cJ0hXisNUVrnVjXnDvnrEIvPKjKfOTrigycw==; kwscode=010115ebdbcf3ecc11856a43173b231fc02feec25611dca95de06c689ceb16ea; kwfv1=PnGU+9+Y8008S+nH0U+0mjPf8fP08f+98f+nLlwnrIP9+Sw/ZFGfzY+eGlGf+f+e4SGfbYP0QfGnLFwBLU80mYG9LE+/GM+nLAPn+jwe4YGfLFweGl+eZEG/ZF8BGAP9L78Bch80QY+0G7GAqA+emY8/DEPfGFGAH7+Aq9+fcE+AW=; kwssectoken=DUJYa6rHJnxHcXgjS8zHwCop/T6FEB9G5t/6aq4YSf8NGyuID2+mdliDni2UQR7mcvyL1ZbTw0efgCZ5D4CysA==; kwscode=c3836572dafa871fbc56056a2cce84cc02ad9e5b5724657af0330341a71eb139; ktrace-context=1|MS44Nzg0NzI0NTc4Nzk2ODY5LjM1MTg3NDY0LjE3NjM4OTI1MTAwMjYuNDUxNzIwNDA=|MS44Nzg0NzI0NTc4Nzk2ODY5Ljc3MTI4Mzg4LjE3NjM4OTI1MTAwMjYuNDUxNzIwNDE=|0|webservice-user-growth-node|webservice|true|src-Js; kpn=KUAISHOU_VISION",
    "referer":"https://www.kuaishou.com/profile/3xpmpj3wr67dsyc?source=PROFILE"
}
pcursor = ""


json_data = {
    "user_id": "3xpmpj3wr67dsyc",
    "pcursor": pcursor,
    "page": "profile"
}
    #发送请求

response = requests.post(url=url,headers=headers,json=json_data)



    #解析数据

feeds = response.json()['feeds']

pcursor = response.json()['pcursor']

if not os.path.exists("video"):
        os.mkdir("video")
for feed in feeds:
        #标题
    caption = feed['photo']['caption']

            #视频链接
    photourl = feed['photo']['photoUrls'][0]['url']
        #print(caption,photourl)
    safe_name01 = caption.replace(" ","")
    safe_name02 = caption.replace("\n","")
    video_data = requests.get(url=photourl,headers=headers).content
 #       for i in range(5):
    with open(f"video/{safe_name02}.mp4","wb")as f:
        f.write(video_data)
        print(f"{safe_name02}保存成功")



























