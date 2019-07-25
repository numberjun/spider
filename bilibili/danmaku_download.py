from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import os
from time import sleep

#改进：自动转成ass字幕形式

#资源：如下
#https://tiansh.github.io/us-danmaku/bilibili/
#这个网站能在线转换xml到ass
#pyautogui
#这个包能控制鼠标点击相应Windows窗口事件


#会下载到这个文件夹C:\Users\Administrator\Downloads
def get_danmaku(fn):
    
    driver = webdriver.Chrome()
    #获取所有已下载的文件名
    allfile = os.listdir(r"C:\Users\Administrator\Downloads")
    #从TXT中读取cids并循环
    with open(fn, "r") as f:
        cids = f.read()

    cids = cids.split("\n")
    cids = cids[:-1]
    for cid in cids:
        cid = cid.split("_")[-1]
        cid = cid+".xml"#文件名(包括后缀)
        #判断这个文件是否已经被下载了
        if cid in allfile:
            print("%s 该文件已存在，跳过下载" % cid)
            continue
        driver.get('http://comment.bilibili.com/%s' % cid);
        sleep(3)
        
        head = driver.find_element("class name","header")

        
        # 执行鼠标动作
        actions = ActionChains(driver)
        # 找到图片后右键单击图片
        actions.context_click(head)
        actions.perform()
        # 发送键盘按键，根据不同的网页，
        # 右键之后按对应次数向下键，
        # 找到图片另存为菜单
        pyautogui.typewrite(['down','down','down','enter'])
        # 单击图片另存之后等1s敲回车
        sleep(2)
        pyautogui.typewrite(['enter'])
        print("已下载%s" % cid)
        

    driver.quit()

#保存cid到danmaku_cid.txt内
def get_cid(url):
    #设置自定义选项
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }
    #新建一个控制窗口
    driver = webdriver.Chrome(desired_capabilities=d)
    
    driver.get(url)
    sleep(3)
    #找到每一集的按钮
    button_list=driver.find_elements("class name","episode-item")
    button_list.append("")

    for button in button_list[1:]:
        sleep(3)
        title = str(driver.title)
        title = title.split("_")[0]
        print(title)
        #等待刷新出弹幕链接包
        sleep(20)
        #从浏览器得到的请求中抽出我们想要的
        for entry in driver.get_log('performance'):
            keys = entry.keys()
            for key in keys:
                if("cid:"in str(entry[

                    key])):
                    flag=0
                    file_name = os.getcwd()+"\\新建文件夹\\"+str(key)
                    with open(file_name+".txt",'w',encoding='utf-8') as f:
                        f.write(str(entry[key]))
                        break
                else:
                    flag=1
            if(flag==0):
                break
        for entry in driver.get_log('performance'):
            pass
        #保存文件之后跳转到新界面
        #从这里开始提取并保存cid到danmaku_cid.txt内
        fn = save_cid(title, file_name+".txt")
        if(button==""):
            pass
        else:
            button.click()
    driver.quit()#关闭浏览器
    return fn

#从这个文件中找出cid并按格式保存
def save_cid(title, filename):
    with open(filename,"r") as f:
        res = f.read()
    first = res.find("cid:")
    last = res.find("&aid")
    cid = res[first+4:last]
    print(cid)
    fn = "danmaku_cid_%s.txt" % title.split("：")[0]
    with open(fn,"a+") as f:
        f.write(title+"_"+cid+"\n")
    return fn


#利用danmaku_cid.txt中的内容，把已下载好的xml文件改名
def change_name(fn):
    with open(fn,"r") as f:
        res = f.read()
    res_list = res.split("\n")
    res_list = res_list[:-1]
    res_dict = {}
    #数字为key，文件名为value
    for re in res_list:
        res_dict[re.split("_")[1]]=re.split("_")[0]
    os.chdir(r"C:\Users\Administrator\Downloads")
    filenames = os.listdir()
    for filename in filenames:
        if(".xml" in filename):
            try:
                new = res_dict[filename.split(".")[0]]
                os.rename(filename,new+".xml")#将工作目录下的某个文件改名
            except KeyError:
                print("不存在%s的保留信息" % filename)
            except FileExistsError:
                print("文件已存在，无法创建 %s" % filename)

if __name__ == "__main__":
    #url为番剧第一集的网址
    url = "https://www.bilibili.com/bangumi/play/ep232367"
    fn = get_cid(url)#获取cid号
    get_danmaku(fn)#获取弹幕文件
    change_name(fn)#修改文件名称与实际对应
