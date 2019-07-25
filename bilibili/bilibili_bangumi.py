import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


SLEEP_TIME=40

def get_url(file_name):
    with open(file_name,'r',encoding="utf-8") as f:
        res = f.read()

    n = res.find('GET')
    res = res[n:]
    m = res.find('url":"')
    n = res.find('"}')
    url = res[m+6:n]
    #print(url)

    #返回url
    return url


def save_fgmp4(url,title,av):
    pa = re.compile('https://(.*?)/upgcxcode')
    host = re.findall(pa,url)[0]
    #print(host)
    
    headers={'Host':host,
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Origin':'https://www.bilibili.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'Referer':'https://www.bilibili.com/bangumi/play/ep%s' % av#av号从最初的input_url中导入
    }
    print("\n正在保存%s" % title)
    
    with open(title+".mp4",'wb') as f:
        f.write(requests.get(url,headers=headers).content)
            

    print("保存完毕\n")


def get_fgsmessage(url,av,logn_flag):
    print("正在开始，多集下载")
    #设置自定义选项
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }
    #新建一个控制窗口
    driver = webdriver.Chrome(desired_capabilities=d)
    
    driver.get(url)
    if(logn_flag):
        logn_flag = input("在弹出的网站登录成功了之后点确定")
    time.sleep(3)
    #找到每一集的按钮
    button_list=driver.find_elements("class name","episode-item")
    button_list.append("")
    #一边循环下载每一集视频一边获取file_title与file_url,以此来检查是否需要重新下载
    file_title_list=[]
    file_url_list=[]
    for button in button_list[1:]:
        time.sleep(8)
        title = str(driver.title)

        print ("Title:" + driver.title)

        if(title.split("_")[0]+".mp4" in os.listdir()):
            driver.get_log('performance')#过滤掉这一集的信息，什么都不做
            print("已存在该文件，跳过保存。。")
            if(button==""):
                pass
            else:
                button.click()
            continue
        
        #添加本次已下载文件名
        file_title_list.append(title.split("_")[0]+".mp4")
        #获取当前页面的url
        file_url_list.append(str(driver.current_url))
        
        #等待刷新出视频链接包
        time.sleep(SLEEP_TIME)
        #从浏览器得到的请求中抽出我们想要的
        for entry in driver.get_log('performance'):
            keys = entry.keys()
            for key in keys:
                if(".flv"in str(entry[key])):
                    flag=0
                    
                    file_name = os.getcwd()+"\\新建文件夹\\"+str(key)
                    with open(file_name+".txt",'w',encoding='utf-8') as f:
                        f.write(str(entry[key]))
                        break
                else:
                    flag=1
            if(flag==0):
                break
        
        #从文件里提取真正的url
        url = get_url(file_name+".txt")
        save_fgmp4(url,title.split("_")[0],av)
        
        
        #保存文件之后跳转到新界面
        if(button==""):
            pass
        else:
            #time.sleep(SLEEP_TIME)
            button.click()
    driver.quit()#关闭浏览器

    #判断文件中是否有需要重新下载的，如果有则重新下载，如果没有，则继续执行
    file_dict = dict(zip(file_title_list,file_url_list))
    reDownload(file_dict)


def reDownload(file_dict):
    
    for file_title in file_dict:
        #获取文件的大小，以此来判断是否需要重新下载
        file_size = os.path.getsize(file_title)
        #如果小于1w字节就重新下载(1024字节=1kB)
        if(file_size < 10000):
            url = file_dict[file_title]
            av=url.split('/')[-1][2:]
            get_fgmessage(url,av,False)


def get_fgmessage(url,av,logn_flag):
    #设置自定义选项
    #如果url是多个(列表)，则爬取多个单集
    print("正在开始，单集下载")
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }
    #新建一个控制窗口
    driver = webdriver.Chrome(desired_capabilities=d)
    driver.get(url)
    if(logn_flag):
        logn_flag = input("在弹出的网站登录成功了之后点确定")
        '''
        cookies = {'buvid3':'6D6FA190-575C-4A1A-81A8-CE4BB0862F2949000infoc',
                   'LIVE_BUVID':'AUTO6215531506011180',
                   'stardustvideo':'1',
                   'CURRENT_FNVAL':'16',
                   'rpdid':'kwxwkxisspdosskoswxpw',
                   'dssid':'93le87628b7bb4bfb',
                   'dsess':'BAh7CkkiD3Nlc3Npb25faWQGOgZFVEkiFTg3NjI4YjdiYjRiZmI4YTEGOwBG%0ASSIJY3NyZgY7AEZJIiViZjUzODMxYjY5MjQzOGVlMzA1OWZhNzBlZjAyNGI5%0AYQY7AEZJIg10cmFja2luZwY7AEZ7B0kiFEhUVFBfVVNFUl9BR0VOVAY7AFRJ%0AIi02OTRjMWY1MTNkNjljYTI5M2RkMDVjYjNiMDAzNTlkZWE0MjNkZWI4BjsA%0ARkkiGUhUVFBfQUNDRVBUX0xBTkdVQUdFBjsAVEkiLWJiMGUwM2Q3ZWEyZDk4%0AYTc1ODA4YmNkYmIxNzgxYWExYmI4NjA0ZTQGOwBGSSIKY3RpbWUGOwBGbCsH%0ALzOTXEkiCGNpcAY7AEYiEzE4Mi4xMDUuMTA5LjU4%0A--fe9235ef356f1a9fdfd0f4861b3a8db7a95e2e72',
                   'UM_distinctid':'1699f001d13469-0853e76e1907f8-54103515-13c680-1699f001d146a2',
                   'fts':'1553150779',
                   'pgv_pvi':'3315162112',
                   'sid':'529gfpbr',
                   'DedeUserID':'12333141',
                   'DedeUserID__ckMd5':'bb6bb4a8c6245dea',
                   'SESSDATA':'fba9ff34%2C1555744015%2Ce23e2431',
                   'bili_jct':'5a25bc118a2ac3ce511dd8a9b0c4148e',
                   'CURRENT_QUALITY':'112',
                   '_dfcaptcha':'84329245ae189e88f8b906b976b7b206',
                   'finger':'edc6ecda'
            }
        
        driver.add_cookie(cookie_dict=cookies)
        '''
        
        driver.get(url)
    time.sleep(8)
    title = str(driver.title)
    print ("Title:" + driver.title)
    
    #等待刷新出视频链接包
    time.sleep(SLEEP_TIME)
    #从浏览器得到的请求中抽出我们想要的
    for entry in driver.get_log('performance'):
        keys = entry.keys()
        for key in keys:
            if(".flv"in str(entry[key])):
                flag=0
                
                file_name = os.getcwd()+"\\新建文件夹\\"+str(key)
                with open(file_name+".txt",'w',encoding='utf-8') as f:
                    f.write(str(entry[key]))
                    break
            else:
                flag=1
        if(flag==0):
            break
    
    #从文件里提取真正的url
    url = get_url(file_name+".txt")
    save_fgmp4(url,title.split("_")[0],av)
    
    driver.quit()#关闭浏览器


def main_fg():
    #ep250650"#测试用(这个可以爬取24分钟)
    #ep96644#ep115338#测试用(这两个都只能爬取6分钟)
    
    input_url = "https://www.bilibili.com/bangumi/play/ep259780"
    av=input_url.split('/')[-1][2:]
    #False代表不连续爬取，即只爬取一个
    flag=False  #True
    #logn_flag代表是否登录
    logn_flag=True
    try:
        if(flag):
            get_fgsmessage(input_url,av,logn_flag)#fgs代表会是一整季番剧
        else:
            get_fgmessage(input_url,av,logn_flag)#fg代表是一集
    except UnboundLocalError:
        print("很抱歉，未能找到视频文件。。")
    

if __name__ == '__main__':
    main_fg()
    
    
    
