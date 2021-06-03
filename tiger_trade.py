import sys 
sys.path.append('./')
import os
import pytest
from os import path
from appium import webdriver
from selenium import webdriver as swebdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from appium.webdriver.common.touch_action import TouchAction
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
SEL_CE = 'http://localhost:4723/wd/hub'

import time, datetime

def init_driver():
    desired_caps = {}

    desired_caps['platformName'] = 'Android'
    desired_caps['deviceName'] = 'emulator-5554'
    desired_caps["platfromVersion"] = "9.0.0"
    desired_caps["autoGrantPermissions"] = True
    # desired_caps['appPackage'] = 'com.google.android.deskclock'
    # desired_caps['appActivity'] = 'com.android.deskclock.DeskClock'

    driver = webdriver.Remote(SEL_CE, desired_caps)
   
    return driver 

def close_current_app(driver):
    try:
        driver.terminate_app(driver.current_package)
    except Exception:
        pass


def wait_click_by_accessibility_id(driver, time, element):
    return wait_click(driver, element,time,  "accessibility_id")

def wait_click_by_id(driver, time, element):
    return wait_click(driver, element,time,  "id")

def wait_click_by_xpath(driver, time, element):
    return wait_click(driver, element, time, "xpath") 

def wait_click(driver, element, time, by):
    i = 0
    text = ""
    sleep(3)
    while i  < time:
        try:
            if by == "accessibility_id":
                ele = driver.find_element_by_accessibility_id(element)
            elif by == "id":
                ele = driver.find_element_by_id(element)
            elif by == "xpath":
                ele = driver.find_element_by_xpath(element)
            ele.click()
            text = ele.text
            # print("find " + element)
            break
        except Exception:
            sleep(3)
            i+=3
    if i == time:
        raise Exception("Can't find " + element)
    else:
        return text


def funcs(driver):
    #open the app
    # el1 = driver.find_element_by_accessibility_id("老虎证券Tiger Trade")
    # el1.click()

    stock_list = []
    stock_list.append(("TTT", 42.27, 239, '买入'))
    stock_list.append(("TTT", 45, 1, '卖出'))
    
    #check the successful order
    trade_list = check_order(driver, stock_list)

    #trade for the cancelled order
    print('to trade today', trade_list)
    for stock_info in trade_list:
        trade(driver, stock_info[0], stock_info[1], stock_info[2], stock_info[3])


def check_order(driver, stock_list):
    back_to_main(driver)

    #query records
    sleep(3)
    el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_trade_image")
    el2.click()

    sleep(3)
    el3 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.TextView")
    el3.click()

    sleep(3)
    el4 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.TextView[2]")
    el4.click()

    sleep(3)    
    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_code")
    record_arr = [dict() for _ in range(len(eles))]
    for i in range(len(eles)):
        record_arr[i]['name'] = eles[i].text
    
    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_orientation")
    for i in range(len(eles)):
        record_arr[i]['orientation'] = eles[i].text
    	
    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_price")
    for i in range(len(eles)):
        record_arr[i]['price'] = float(eles[i].text)

    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_quantity")
    for i in range(len(eles)):
        record_arr[i]['count'] = int(eles[i].text)

    
    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_deal_date")
    for i in range(len(eles)):
        record_arr[i]['date'] = eles[i].text

    # print(record_arr)
    new_list = []
    for dic in record_arr:
        if time_ok(dic['date']):
            if (dic['name'], dic['price'], dic['count'], dic['orientation']) in stock_list:
                print('traded', dic)
                stock_list.remove((dic['name'], dic['price'], dic['count'], dic['orientation']))
    return stock_list
    
def trade(driver, stock_name, stock_price, stock_count, direction):
    back_to_main(driver)

    try:
        el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_market_image")
        el2.click()
    except:
        pass
    #search
    el3 = driver.find_element_by_id("com.tigerbrokers.stock:id/fab_image_btn_right_2")
    el3.click()
    sleep(3) 
    el4 = driver.find_element_by_id("com.tigerbrokers.stock:id/edit_ab_search_stock")
    el4.send_keys(stock_name)
    while True:
        try:
            sleep(3)
            el5 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.LinearLayout")
            el5.click()
            break
        except:
            pass
    sleep(3) 
    el6 = driver.find_element_by_id("com.tigerbrokers.stock:id/image_tabbar_account_type")
    el6.click()
    sleep(3) 

    #buy or sell
    if direction == '买入':
        el7 = driver.find_element_by_id("com.tigerbrokers.stock:id/bg_image_buy_in")
        el7.click()
    else:
        el7 = driver.find_element_by_id("com.tigerbrokers.stock:id/bg_image_sell")
        el7.click()
    sleep(3)

    # edit the price and amount
    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/edit_number")
    eles[0].send_keys(str(stock_price))
    eles[1].send_keys(str(stock_count))

    sleep(3) 
    el9 = driver.find_element_by_id("com.tigerbrokers.stock:id/btn_place_order_submit")
    el9.click()

def back_to_main(driver):
    #go back
    # el1 = driver.find_element_by_id("com.tigerbrokers.stock:id/fab_image_btn_left")
    # el1.click()
    # sleep(3) 
    while True:
        try:
            el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_market_image")
            el2.click()
            return
        except Exception as e:
            try:
                el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_market_lottie")
                return
            except Exception:
                driver.press_keycode(4)
                sleep(3)

def time_ok(tss1):
    # 转为时间数组
    timeArray = time.strptime(tss1, "%Y/%m/%d")
    timeStamp = int(time.mktime(timeArray))
    now = int(time.time())
    if (now - timeStamp) < 86400 * 7:
        return True
    return False
    
def run1():
    driver = init_driver()
    funcs(driver)

run1()