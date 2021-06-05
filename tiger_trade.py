from genericpath import exists
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

def check_order(driver, stock_list, cash=False):
    back_to_main(driver)

    #query records
    sleep(3)
    el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_trade_image")
    el2.click()

    #click order
    sleep(3)
    if cash:
        el3 = driver.find_element_by_id("com.tigerbrokers.stock:id/stock_trade_entry_order")
        el3.click()
    else:
        el3 = driver.find_element_by_id("com.tigerbrokers.stock:id/layout_btn_virtual_trade_order")
        # el3 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.TextView")
        el3.click()

    #已成交
    sleep(3)
    if cash:
        el4 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.TextView[2]")
        el4.click()
    else:
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
                append_history_orders([(dic['name'], dic['price'], dic['count'], dic['orientation'], dic['date'])], cash)
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

    input_trade_pass(driver)

    # edit the price and amount
    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/edit_number")
    eles[0].send_keys(str(stock_price))
    eles[1].send_keys(str(stock_count))

    sleep(3) 
    el9 = driver.find_element_by_id("com.tigerbrokers.stock:id/btn_place_order_submit")
    el9.click()

def input_trade_pass(driver):
    com.tigerbrokers.stock:id/title
    if ele.text == "请输入交易密码":

def back_to_main(driver):
    #advertisement
    try:
        el1 = driver.find_element_by_accessibility_id("关闭弹框")
        el1.click()
    except:
        pass

    # open the app
    try:
        el1 = driver.find_element_by_accessibility_id("老虎证券Tiger Trade")
        el1.click()
        sleep(6)
    except:
        pass

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
    
def read_orders(cash=False):
    orders = []
    order_path = "orders.txt"
    if cash == True:
        order_path = "cash_orders.txt"
    with open(order_path, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            try:
                params = line.split(",")
                code = params[0].split("=")[1].strip()
                price = float(params[1].split("=")[1])
                count = int(params[2].split("=")[1])
                direction = params[3].split("=")[1].strip()
                orders.append((code, price, count, direction))
            except:
                pass
    return orders

def update_orders(updated_orders, cash=False):
    order_path = "orders.txt"
    if cash == True:
        order_path = "cash_orders.txt"
    if not os.path.exists(order_path):
        with open(order_path, "w"):
            pass
    with open (order_path, "w", encoding="utf-8") as f:
        for order in updated_orders:
            f.write(f"code={order[0]},price={order[1]},count={order[2]}, direction={order[3]}\n")

def append_history_orders(history_orders, cash=False):
    history_order_path = "history_orders.txt"
    if cash == True:
        history_order_path = "cash_history_orders.txt"
    if not os.path.exists(history_order_path):
        with open(history_order_path, "w"):
            pass
    with open (history_order_path, "a", encoding="utf-8") as f:
        for order in history_orders:
            f.write(f"code={order[0]},price={order[1]},count={order[2]}, direction={order[3]}, date={order[4]}\n")

def close_current_app(driver):
    try:
        driver.terminate_app(driver.current_package)
    except Exception:
        pass

def switch_account(driver, cash=False):
    back_to_main(driver)
    sleep(2)
    el2 = driver.find_element_by_id("com.tigerbrokers.stock:id/text_main_bottom_trade_image")
    el2.click()
    sleep(2)
    el3 = driver.find_element_by_id("com.tigerbrokers.stock:id/fab_text_action_left")
    el3.click()
    sleep(2)
    eles = driver.find_elements_by_id("com.tigerbrokers.stock:id/account_title")
    print(len(eles))
    if cash == True:
        eles[0].click()
    else:
        eles[1].click()


def run():
    cash = True

    orders = read_orders(cash)
    print("read", orders)

    driver = init_driver()
    switch_account(driver, cash)
    #check the successful order
    trade_list = check_order(driver, orders, cash)
    update_orders(trade_list, cash)
    #trade for the cancelled order
    print('to trade today', trade_list)
    for stock_info in trade_list:
        trade(driver, stock_info[0], stock_info[1], stock_info[2], stock_info[3])
    close_current_app(driver)
run()