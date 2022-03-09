import requests

# 请求头部
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"}
proxies = { "http": None, "https": None}
## 拿到下载地址
urls = [
    'http://s3.ananas.chaoxing.com/doc/d1/42/8a/c5b549381594f5b6546641304a924b4b/thumb/', # 2.4   2_4_1  表示2.4的ppt的第一张图片

    'http://s3.ananas.chaoxing.com/doc/02/73/34/30a261a568551e5615701371b302abe4/thumb/', # 2.5 同理下
    
    'http://s3.ananas.chaoxing.com/doc/ef/fc/f0/fff56ac37b0bd295596c7854d602cea8/thumb/', # 3.1

    'http://s3.ananas.chaoxing.com/doc/08/a1/51/b1904e28382e85e455bdcb2cccf80ab6/thumb/', # 3.2

    'http://s3.ananas.chaoxing.com/doc/b5/c5/e4/79e7042698f301f23139fb571ebe6f32/thumb/', # 3.3

    'http://s3.ananas.chaoxing.com/doc/e9/4c/32/b2690224d9f034acefca10a7b74459d7/thumb/', # 3.4
]
paras = [
    '2_4',
    '2_5',
    '3_1',
    '3_2',
    '3_3',
    '3_4',
]
## 改变参数实现每个课件图片的输出
for url,para in zip(urls,paras):

    for num in range(1,101):
        href = url+str(num)+'.png'
        response = requests.get(href,timeout=5,headers=headers,proxies=proxies)
        # 即图片不存在
        if response.status_code != 200:
            pass
        else:
            filename =para +'_'+str(num)+'.png'
            with open(filename,'wb') as f:
                f.write(response.content)
                print("[download success] " + response.url)



## 批量下载图片
   # 判断图片地址是否存在
   # 存在下载，不存在pass
