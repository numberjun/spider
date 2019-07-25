# 不知道如何划分第几话

import os
from mitmproxy import ctx

def response(flow):
    # 手动分析得到漫画的接口
    url = 'https://i0.hdslb.com/bfs/manga'
    # 保存漫画的文件夹
    file_path = r'C:\Users\Administrator\Desktop\pic'
    # 获取该文件夹内的文件名
    files = os.listdir(file_path)
    # 得到这一页漫画要保存的文件名
    file_name = str(flow.request.url).split(r'%')[-1] + '.jpg'
    # 如果是该接口且是jpg的文件则将其二进制存入文件夹中
    # 以时间查看就能按顺序/或者os.listdir()也是按顺序
    if flow.request.url.startswith(url):
        if '.jpg' in str(flow.request.url):
            res = flow.response.content
            if file_name in files:
                file_name = file_name.split('.')[0]+'0'+'.jpg'
            with open(file_path+"\\"+file_name, 'wb') as f:
                f.write(res)
