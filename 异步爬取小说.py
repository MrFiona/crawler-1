#https://dushu.baidu.com/api/pc/getDetail?data={"book_id":"4316251006"}
# https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4316251006","cid":"4316251006|11070660","need_bookinfo":1}
import requests
import asyncio
import aiohttp
import jsonpath
import json
import aiofiles
import time

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
}

async def aiodownload(cid,b_id,title):
    data = {
        "book_id":b_id,
        "cid":f"{b_id}|{cid}",
        "need_bookinfo":1
    }

    data = json.dumps(data)
    url = f"https://dushu.baidu.com/api/pc/getChapterContent?data={data}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic = await resp.json()
            
            async with aiofiles.open(title+".txt",mode='w',encoding='utf-8') as f:
                print(dic['data']['novel']['content'])
                await f.write(dic['data']['novel']['content'])

async def getCid(url):
    
    tasks = []
    r = requests.get(url,headers=headers,verify=False)
    jsonData = r.json()
    cids = jsonpath.jsonpath(jsonData, '$..cid')
    titles = jsonpath.jsonpath(jsonData,'$..title')
    
    for cid,title in zip(cids,titles):
        tasks.append(asyncio.create_task(aiodownload(cid,b_id,title)))
    # print(cids,titles)
    await asyncio.wait(tasks)


if __name__ == '__main__':

    start = time.time()
    b_id = 4316251006
    url = 'https://dushu.baidu.com/api/pc/getDetail?data={"book_id":"'+str(b_id)+'"}'
    asyncio.run(getCid(url))
    
    end = time.time()
    print("cost time:%f" %(end -  start))