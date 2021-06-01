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

    #query records
    # sleep(3)
    # el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_trade_image")
    # el2.click()

    # sleep(3)
    # el3 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.TextView")
    # el3 = driver.find_element_by_accessibility_id("订单")
    # el3.click()

    sleep(3)
    # el4 = driver.find_element_by_accessibility_id("已成交")
    # el4 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.TextView[2]")
    # el4.click()

    sleep(3)    
    # eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_name")
    # record_arr = [dict() for _ in range(len(eles))]
    # for i in range(len(eles)):
    #     record_arr[i]['name'] = eles[i].text
    
    # eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_orientation")
    # for i in range(len(eles)):
    #     record_arr[i]['orientation'] = eles[i].text
    	
    # eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_price")
    # for i in range(len(eles)):
    #     record_arr[i]['price'] = eles[i].text
    
    # eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/text_item_order_history_deal_date")
    # for i in range(len(eles)):
    #     record_arr[i]['date'] = eles[i].text

    # print(record_arr)
    # for dic in record_arr:
    #     if time_ok(dic['date']):
    #         print('traded', dic)

    #3. trade now
    #go back
    el1 = driver.find_element_by_id("com.tigerbrokers.stock:id/fab_image_btn_left")
    el1.click()
    
    el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_market_image")
    el2.click()
    el3 = driver.find_element_by_id("com.tigerbrokers.stock:id/fab_image_btn_right_2")
    el3.click()
    el4 = driver.find_element_by_id("com.tigerbrokers.stock:id/edit_ab_search_stock")
    el4.send_keys("TTT")
    el5 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.LinearLayout")
    el5.click()
    el6 = driver.find_element_by_id("com.tigerbrokers.stock:id/image_tabbar_account_type")
    el6.click()
    el7 = driver.find_element_by_id("com.tigerbrokers.stock:id/bg_image_buy_in")
    el7.click()
    el8 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.EditText")
    el8.send_keys("40")
    el9 = driver.find_element_by_id("com.tigerbrokers.stock:id/btn_place_order_submit")
    el9.click()
    el10 = driver.find_element_by_id("com.tigerbrokers.stock:id/place_order_holdings_and_orders_market")
    el10.click()

    

    com.tigerbrokers.stock:id/edit_number

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