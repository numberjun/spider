import os
import time
from appium import webdriver
from multiprocessing import Process
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(user,pwd,wait):
    index = wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[4]/android.view.View/android.widget.ImageView')))
    index.click()
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/wh')))
    index.click()
    time.sleep(1)
    set_index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/ga')))
    set_index.set_text(user)
    time.sleep(2)
    set_index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/g4')))
    set_index.set_text(pwd)
    time.sleep(1)
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/c6')))
    index.click()
    time.sleep(2)
    index = wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[1]/android.view.View/android.widget.ImageView')))
    index.click()


def bilimanhua(key_word,direction):
    # 设置方向
    if direction == 'right':
        fx = 0.25  # 向右翻页(日漫)
    else:
        fx = 0.75  # 向左翻页(普通)


    # 连接上appium(要先开启appium)
    server = "http://localhost:4723/wd/hub"

    # 设置手机和要打开的APP的属性，设置接受Unicode字符
    desired_caps = {
      "platformName": "Android",
      "deviceName": "SM_G955F",
      "appPackage": "com.bilibili.comic",
      "appActivity": ".view.MainActivity",
      'unicodeKeyboard':True,
      "resetKeyboard": True
    }

    # 设置等待时间和driver
    driver = webdriver.Remote(server, desired_caps)
    wait = WebDriverWait(driver,30)

    # 设置点击的位置,由此来控制方向
    width_point = driver.get_window_size()['width'] * fx
    height_point = driver.get_window_size()['height'] * fx



    # 点 关闭弹窗
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/cp')))
    index.click()
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/cp')))
    index.click()

    # 登录，不想登录也能注释跳过
    username=''  #请输入自己的B站账号
    password=''  #请输入自己的B站密码
    login(username,password,wait)
    
    # 点击搜索框
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/y5')))
    index.click()
    # 输入
    set_index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/gz')))
    set_index.set_text(key_word)
    # 点第一个
    index = wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]')))
    index.click()
    # 点进漫画
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/vy')))
    index.click()
    
    '''
    # 点第一章
    index = wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.Button')))
    index.click()
    '''
    # 点 更多
    index = wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.ImageButton')))
    index.click()
    # 点 上次看到的地方
    index = wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[13]/android.widget.Button')))
    index.click()
    


    # 点  知道了
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/jd')))
    index.click()
    # 点  消除下面一行
    index = wait.until(EC.presence_of_element_located((By.ID, 'com.bilibili.comic:id/jd')))
    index.click()

    i = 0
    while True:
        # 请参照下面自己编写退出条件（是需要购买后立即退出还是自动购买
        time.sleep(2)
        driver.tap([(width_point, height_point)], 500)
        '''
        # 点击到登录购买之后，右上角会出现转发的字样
        res = driver.page_source
        # 如果出现转发字样，则跳出循环，结束程序
        if 'com.bilibili.comic:id/k5' in res:
            print('END')
            break
        '''
        print(i)
        i += 1


def mitmdump_begin():
    os.system("mitmdump -s mitmdump_bilibilimanga.py")

if __name__ == "__main__":
    mitmdump_process = Process(target=mitmdump_begin)
    mitmdump_process.start()
    
    key_word = '四月是你的谎言'  # "天才们的恋爱头脑战"
    direction = 'right'  # 翻页的方向，只有left和right,向右翻页(日漫),向左翻页(普通)

    bilimanhua(key_word,direction)
    

