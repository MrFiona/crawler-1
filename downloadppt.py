# -*- coding: utf-8 -*-
import requests
import pprint
import re
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "close",
    "Referer": "http://down1.5156edu.com/",
    "Cookie": "zmj66=4; zmj77=1",
    "Upgrade-Insecure-Requests": "1"
}

# mainPageUrl = 'http://www.5156edu.com/html2/16045.html'
# reponse = requests.get(mainPageUrl)
# reponse.encoding = 'gbk'

# mainPageSource = reponse.content

# 获取每个课件第一页面链接
# soup = BeautifulSoup(mainPageSource,"html.parser")
# alist = soup.find_all("a")
# for a in alist:
#     href = a['href']
#     # print(href)

# 读取文件中的链接，拼接起来
# firstList = []
# with open('hrefs.txt','r') as f:
#     lines = f.readlines()
#     for line in lines:
#         line = line.strip('\n')
#         line = 'http://www.5156edu.com'+line
#         firstList.append(line)

# # print(firstList)
# # re解析获取到每个课件下载的页面
# # <b>课件</b></div>&nbsp;<a href='/page/21-03-31/178041.html' target="_blank" >《灯笼》pptx课件（34页）</a>
# for downloadPageUrl in firstList:
#     reponse = requests.get(downloadPageUrl)
#     try:
#         reponse.encoding = 'gbk'
#         source = reponse.text

#         # print(source)
#         # break
#         # re解析获取下载页面

#         print("[*]"+downloadPageUrl)
#         obj = re.compile(r"<b>课件</b></div>&nbsp;<a href='(?P<dlUrl>.*?)'(.*?)ppt(.*?)</a>",re.S)
#         result = obj.finditer(source)

#         urlList = []
#         for url in result:
#             url = url.group('dlUrl')
#             url = 'http://www.5156edu.com'+url
#             urlList.append(url)
#         print(urlList[0])
#         dlUrl = urlList[0]
#         with open('downloadUrl.txt','a') as f:
#             f.write(dlUrl+'\n')
#     except Exception as e:
#         print('error:',e)

# 从每个课件的下载页面中获取下载链接，并且获取当前课件的名字，给压缩包命名
def main():
    with open('downloadUrl.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            
            response = requests.get(line,headers=headers,timeout=5)
            response.encoding = 'gbk'
            source = response.text
            
            # 获取最终下载课件的地址
            # <font color=#cc9966>《灯笼》pptx课件（34页）</font>
            # <font color=#cc9966>《登勃朗峰》ppt课件（14页）</font>
            # <a href=http://down1.5156edu.com/showzipdown.php?id=169615><font color=red><u>点击本地免费下载</u></font>
            # <a href=http://down5.5156edu.com/showzipdown4.php?f_type1=2&id=169615><font color=red><u>本地免费下载1</u></font>
            # <a href=http://down8.5156edu.com/showzipdown4.php?f_type1=2&id=18206><font color=red><u>本地下载1</u></font></a>
            obj0 = re.compile(r"<font color=#cc9966>(?P<name>.*?)</font>",re.S)
            obj1 = re.compile(r"<a href=(?P<dlUrl0>.*?)<font color=red><u>点击本地免费下载</u></font>")
            obj2 = re.compile(r"<a href=(?P<dlUrl1>.*?)><font color=red><u>本地(.*?)</u></font>")
            
            result0 = obj0.finditer(source)
            result1 = obj1.finditer(source)
            
            nameList = [] # 保存文件名列表
            urlList = []  # 下载页面
            dlList = []   # ppt下载链接

            for name in result0:
                name = name.group('name')
                print('[*]'+name)
                with open('pptname.txt','a') as f:
                    f.write(name+'\n')

                nameList.append(name)

            for url in result1:
                url = url.group('dlUrl0')
                # print(url)
                urlList.append(url)

            # 从下载页面中获取ppt压缩包下载地址
            for url in urlList:
                # print(url)
                response = requests.get(url,headers=headers,timeout=5)
                response.encoding = 'gbk'
                source = response.text 
                
                result = obj2.search(source)
                # print(result.group('dlUrl1'))
                dlUrl = result.group('dlUrl1')

                with open('dlUrl.txt','a') as f:
                    f.write(dlUrl+"\n")
                
                # 下载ppt
                response = requests.get(dlUrl,headers=headers,timeout=10)
                for name in nameList:

                    with open(f'{name} '+'.zip','wb') as f:
                        f.write(response._content)
                        print('download'+name+' over!')

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    cost = end - start 
    urlcount = len(open('dlUrl.txt','r').readlines()) 
    print('count: '+ str(urlcount) +'条' + 'cost time: '+str(cost) +'s')


        

            
        


