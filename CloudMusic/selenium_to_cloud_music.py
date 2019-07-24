from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
import requests
import os

def get_url(file_name):

    with open(file_name,'r',encoding='utf-8')as f:
        zero = f.read()

        while(True):
            num = zero.find('.m4a')
            mid = zero[num-150:num+4]
            if('url":"' in mid):
                url_num = zero[num-150:num+4].find('url":"')
                res = mid[url_num+6:]
                break
            else:
                zero = zero[num+4:]
    print(res)
    return res

def get_message(url):
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }
    driver = webdriver.Chrome(desired_capabilities=d)
    
    driver.get(url)
    time.sleep(3)
    print ("Title:" + driver.title)
    
    title = str(driver.title)
    fn = title.split(" - ")[0]
    print(fn)

    #找有没有这个文件名 title+".txt" 的文件
    for i in os.listdir():
        if( fn+".txt" in i):
            print("本地已经存在该文件")
            return fn+".txt"
    
    driver.switch_to_frame('g_iframe')# 网易云的音乐元素都放在框架内！！！！先切换框架
    register = driver.find_element_by_css_selector("[class='u-btn2 u-btn2-2 u-btni-addply f-fl']")
     
    register.click()
    time.sleep(7)

    for entry in driver.get_log('performance'):
        keys = entry.keys()
        for key in keys:
            if('.m4a' in str(entry[key])):
                flag=0
                
                
                with open(fn+".txt",'w',encoding='utf-8') as f:
                    f.write(str(entry[key]))
                    break
            else:
                flag=1
        if(flag==0):
            break

    driver.quit()#关闭浏览器
    return fn+".txt"

def save_mp3(url,file_name):
    headers = {'user-agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
    res = requests.get(url,headers = headers)
    with open(file_name[:-4]+'.m4a','wb') as f:
        f.write(res.content)
    print("保存完成文件："+file_name[:-4]+".m4a")

if __name__ == '__main__':
    #用户从这里输入，想输入名字的话也可以加一个
    input_url = "https://music.163.com/#/song?id=1377450530"
    file_name = get_message(input_url)
    url = get_url(file_name)#该url为真正的下载界面
    save_mp3(url,file_name)
    
