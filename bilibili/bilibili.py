import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException , NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0




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

def save_mp4(url,av,title):
    pa = re.compile('https://(.*?)/upgcxcode')
    host = re.findall(pa,url)[0]
    #print(host)
    
    headers={'Host':host,
    'Connection':'keep-alive',
    'Origin':'https://www.bilibili.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'Accept':'*/*',
    'Referer':'https://www.bilibili.com/video/av%s' % av,#av号从最初的input_url中导入
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9'
    }
    with open(title+"_"+av+".mp4",'wb') as f:
        f.write(requests.get(url,headers=headers).content)
    return headers

def get_message(url,av):
    #设置自定义选项
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }
    #新建一个控制窗口
    driver = webdriver.Chrome(desired_capabilities=d)
    
    driver.get(url)
    driver.set_window_size(1280,800)
    time.sleep(3)    
    title = str(driver.title)
    print ("Title:" + driver.title)
    
    #找分p，如果没有分p则获取报错信息
    try:
        zk = driver.find_element_by_css_selector("[class='item v-part-toggle']")#可以使用复合类名
        zk.click()
        time.sleep(4)
        i_list = driver.find_elements("class name","item")
        for n,i in enumerate(i_list):
            if(i.get_attribute("href") == None):
                pass
            else:
                flag=n
                break
        i_list = i_list[n+1:]
    except NoSuchElementException:
        print("没有找到分p，只获取当前页面的视频")
        i_list=[]
        i_list.append("")
    i_list.append("")

    #准备开始下载
    for n,i in enumerate(i_list):
        time.sleep(60)
        

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

        
        url = get_url(file_name+".txt")#从文件里提取真正的url
        save_mp4(url,av,title.split("_")[0]+"_"+str(n))#开始下载
        if(i_list[n]==""):
            pass
        else:
            i_list[n].click()
    driver.quit()#关闭浏览器        

#使用修改url
def main0():
    input_url = "https://www.bilibili.com/video/av160825"
    #input_url = "https://www.bilibili.com/video/av2981393"
    av=input_url.split('/')[-1][2:]
    try:
        get_message(input_url,av)
    except UnboundLocalError:
        print("很抱歉，未能找到视频文件。。")

    

#使用添加TXT
def main():
    
    with open('av号.txt','r') as f:
        av_list = f.readlines()
    for av in av_list:
        input_url = "https://www.bilibili.com/video/av%s" % av[:-1]
        try:
            get_message(input_url,av)
        except UnboundLocalError:
            print("很抱歉，未能找到视频文件,可能是网络延迟原因。。")
            print("程序将暂停三分钟，然后再次爬取")
            time.sleep(180)
            continue

if __name__ == '__main__':
    #main0使用url
    #main使用TXT
    main0()
    
    
    
