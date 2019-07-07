__author__ = '数字菌'

'''
项目：网易云音乐下载
程序功能：通过音乐id访问音乐原始地址实现下载
'''
import os
import time
import requests
from bs4 import BeautifulSoup

  
# 建立一个歌单的文件夹并切换运行目录
def new_dir(title):
    if os.path.exists(title):
        print('歌单文件夹已存在,开始提取歌曲信息')
    else:
        os.mkdir(title)
        print('创建歌单文件夹')
    os.chdir(title)


# 通过歌单获取音乐id与歌名列表，并切换目录
def get_music_list(url):
    # 在这里判断url中是否有/#/这个东西，如果有，把它变换成/
    if '/#/' in url:
        url = url.replace('/#/','/')
        
    # 设置music_id_list music_name_list
    music_id_list = []
    music_name_list = []
    
    headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
    res = requests.get(url=url,headers=headers)
    
    soup = BeautifulSoup(res.text,'lxml')

    # 建立一个歌单的文件夹
    new_dir(soup.title.text)
    
    ul = soup.find_all('ul',{'class':'f-hide'})
    for a in ul[0].find_all('a'):
        # 这里每一个a是一个a标签（bs4的tag类型），里面有歌名和歌曲id
        music_a_id = a['href']  # /song?id=*****
        music_id_list.append(music_a_id[music_a_id.find('=')+1:])
        music_name_list.append(a.text)  # 歌名

    return (music_id_list,music_name_list)


# 通过单曲获取音乐id与歌名列表，并切换目录
def get_single_list(url):
    '''
    访问单曲网页获得信息
    url = https://music.163.com/#/song?id=462605322
    '''
    if '/#/' in url:
        url = url.replace('/#/','/')
    music_id_list = []
    music_name_list = []
    
    headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
    res = requests.get(url=url,headers=headers)
    
    soup = BeautifulSoup(res.text,'lxml')
    music_id = url[url.find('?id=')+4:]
    music_id_list.append(music_id)
    music_name_list.append(soup.find('em',{'class':'f-ff2'}).text)
    return (music_id_list,music_name_list)


# 获取歌曲
def get_music(music_id_list,song_name_list):
    url = "http://music.163.com/song/media/outer/url"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }

    params = {}
    for i in range(len(music_id_list)):
        song_name_list[i] = song_name_list[i].replace("/"," ").replace("\\"," ").replace(":","：").replace("?","？").replace('"',' ').replace("*"," ").replace("<","《").replace(">","》").replace("|"," ")
        #如果歌曲已存在则跳过这一步
        if os.path.exists('{name}.mp3'.format(name=song_name_list[i])):
            print("歌曲:{name} 已存在，跳过下载步骤".format(name=song_name_list[i]))
            continue

        time.sleep(1)
        params['id']='{m_id}.mp3'.format(m_id=music_id_list[i])
        res = requests.get(headers=headers,url=url,params=params)
        real_url = res.url
        if "m10.music.126.net" in real_url:
            # 成功跳转则下载
            with open('{name}.mp3'.format(name=song_name_list[i]),'wb') as f:
                f.write(res.content)
            print('下载完成:{name}'.format(name=song_name_list[i]))
        elif "/404" in real_url:
            # 出现404
            print("未找到该歌曲的下载页面")
        else:
            # 出现未知问题
            print("出现了未知的跳转界面，跳转结果为：")
            print(real_url)
        

if __name__ == "__main__":
    sin = input("请输入0（歌单）或1（单曲）后开始下载:")
    if sin == '0':
        list_url = input("请输入歌单的网址：")
        music_id_list,music_name_list = get_music_list(list_url)  # 获取歌曲id列表与名字列表
        get_music(music_id_list,music_name_list)
        print('下载完成')
    elif sin == '1':
        '''
        默认id与name都是list，单曲也是一个长度为1的list
        '''
        music_url = input('请输入单曲的网址：')
        music_id_list,music_name_list = get_single_list(music_url)
        get_music(music_id_list,music_name_list)
        print('下载完成')
    else:
        print('输入有误，程序结束')

