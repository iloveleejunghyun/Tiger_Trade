# -*- encoding=utf8 -*-
#todo 目前只支持一个股票一个挂单（买入/卖出分别一个），因为实际买入卖出价格可能与挂单价不同，不好判断。

__author__ = "Administrator"

from airtest.core.api import *

auto_setup(__file__)


import time, datetime, os
from util import * 

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

dev = connect_device("android://127.0.0.1:5037/127.0.0.1:62001?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MINITOUCH")

    
def back_to_main():
    pwait_click("com.tigerbrokers.stock:id/btn_cancel", times=1)

    #advertisement
    pwait_click(text="关闭弹框",times=1)

    for _ in range(3):
        if not pwait_click("com.tigerbrokers.stock:id/text_main_bottom_market",times=1): #有广告的时候能否找到这个?
            pwait_click("com.tigerbrokers.stock:id/btn_cancel", times=1)
            pwait_click(text="关闭弹框",times=1)
            keyevent("KEYCODE_BACK")
            sleep(0.5)
        else:
            return
            
def check_order(orders, stock_list, cash=False):
    back_to_main()

    pwait_click("com.tigerbrokers.stock:id/text_main_bottom_trade")
    pwait_click(text="订单")
    #已成交
    if not pwait_click(text="已成交"):
        screenshot('No已成交')
    if not pwait_until("com.tigerbrokers.stock:id/text_item_order_history_code"):
        logger.error("没有找到历史订单，退出")
        return orders
    
    eles = poco("com.tigerbrokers.stock:id/text_item_order_history_code")
        
    record_arr = [dict() for _ in range(len(eles))]
    for i in range(len(eles)):
        record_arr[i]['code'] = eles[i].get_text()
    
    eles = poco("com.tigerbrokers.stock:id/text_item_order_history_orientation")
    for i in range(len(eles)):
        record_arr[i]['orientation'] = eles[i].get_text()
    	
    eles = poco("com.tigerbrokers.stock:id/text_item_order_history_price")
    for i in range(len(eles)):
        record_arr[i]['price'] = float(eles[i].get_text())

    eles = poco("com.tigerbrokers.stock:id/text_item_order_history_quantity")
    for i in range(len(eles)):
        record_arr[i]['count'] = int(eles[i].get_text())

    eles = poco("com.tigerbrokers.stock:id/text_item_order_history_deal_date")
    for i in range(len(eles)):
        record_arr[i]['date'] = eles[i].get_text()

    # logger.info(record_arr)
    new_list = []
    for dic in record_arr:
        if time_ok(dic['date']):
            if (dic['code'], dic['count'], dic['orientation']) in stock_list:
                logger.info(f'traded {dic}')
                for order in orders:
                    if order[0] == dic['code'] and order[2] == dic['count'] and order[3] == dic['orientation']:
                        orders.remove(order)
                        break
                stock_list.remove((dic['code'], dic['count'], dic['orientation']))
                append_history_orders([(dic['code'], dic['price'], dic['count'], dic['orientation'], dic['date'])], cash)
    return orders

def time_ok(tss1):
    # 转为时间数组
    timeArray = time.strptime(tss1, "%Y/%m/%d")
    timeStamp = int(time.mktime(timeArray))
    now = int(time.time())
    if (now - timeStamp) < 86400 * 3: #最近3天
        return True
    return False

def read_orders(cash=False):
    orders = []
    stock_list = []
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
                stock_list.append((code, count, direction))
            except:
                pass
    return orders,stock_list

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

def switch_account(cash=False):
    back_to_main()
    
    if not pwait_click("com.tigerbrokers.stock:id/text_main_bottom_trade"):
        screenshot('NoBottomTrade')

    if not pwait_click("com.tigerbrokers.stock:id/fab_text_action_left"):
        screenshot('NoSwitchLeft')
    pwait_until("com.tigerbrokers.stock:id/account_title")
    eles = poco("com.tigerbrokers.stock:id/account_title")
#     logger.info(len(eles))
    if cash == True:
        eles[0].click()
#         pwait_click(text="综合账户")
#         pwait_click("com.tigerbrokers.stock:id/stock_trade_entry_deal")
        logger.info("Switch to cash account")
        pwait_click('com.tigerbrokers.stock:id/trade_entry_point')
        if pwait_until(text='请输入交易密码'):
            input_trade_pass()
            if pwait_until(text='买入下单', times=2):
                keyevent("KEYCODE_BACK")
    else:
        eles[1].click()
#         pwait_click(text="老虎模拟账户")
        logger.info("Switch to simulation account")
    #如果左边匡没有关闭，则关闭
        
def trade(stock_code, stock_price, stock_count, direction):
    try:
        back_to_main()

        pwait_click(text="行情")

        #search
        pwait_click("com.tigerbrokers.stock:id/fab_image_btn_right_2")
        pwait_until("com.tigerbrokers.stock:id/edit_ab_search_stock")
        poco("com.tigerbrokers.stock:id/edit_ab_search_stock").set_text(stock_code)
        pwait_until("com.tigerbrokers.stock:id/text_search_stock_code")
        pwait_click("com.tigerbrokers.stock:id/text_search_stock_code")
        pwait_click("com.tigerbrokers.stock:id/text_tabbar_trade")

        #buy or sell
        if direction == '买入':
            pwait_click("com.tigerbrokers.stock:id/bg_image_buy_in")
        else:
            pwait_click("com.tigerbrokers.stock:id/bg_image_sell")

        if pwait_click(text="取消"):
            logger.info(f"{stock_code}已经有订单了，取消")
            return

        pwait_until("com.tigerbrokers.stock:id/edit_number")
        # edit the price and amount
        eles = poco("com.tigerbrokers.stock:id/edit_number")
        eles[0].set_text(str(stock_price))
        sleep(2)
        eles[1].set_text(str(stock_count))
        sleep(2)
        
        pwait_click("com.tigerbrokers.stock:id/btn_place_order_submit")
        logger.info(f"{stock_code}挂单成功")
    except Exception as e:
        logger.info(e)
        screenshot('TradeFail')

# eles = poco("com.tigerbrokers.stock:id/edit_number")
# print(eles)
# eles[0].set_text(str(1))
# eles[1].set_text(str(2))
# sleep(100)
def input_trade_pass():
    keyevent("KEYCODE_3")
    keyevent("KEYCODE_2")
    keyevent("KEYCODE_1")
    keyevent("KEYCODE_6")
    keyevent("KEYCODE_5")
    keyevent("KEYCODE_4")

def check_update():
    if pwait_click("com.tigerbrokers.stock:id/btn_dialog_update_positive"):
        if pwait_until("com.android.packageinstaller:id/ok_button",times=30):
            pwait_click("com.android.packageinstaller:id/ok_button")
            if pwait_until("com.android.packageinstaller:id/launch_button",times=30):
                pwait_click("com.android.packageinstaller:id/launch_button")
                sleep(10)

def run():
#     pwait_until("com.tigerbrokers.stock:id/btn_cancel", times=1)

    #advertisement
#     pwait_until(text="关闭弹框",times=1)

#     for _ in range(5):
#     pwait_until("com.tigerbrokers.stock:id/text_main_bottom_market",times=1) #有广告的时候能否找到这个?
#             pwait_click(text="关闭弹框",times=1)
#     sleep(500)
#     switch_account(False)
    try:
        logger.info("start to trade")
        stop_app("com.tigerbrokers.stock")
        sleep(5)
        start_app("com.tigerbrokers.stock")
        sleep(10)
        back_to_main()
        check_update()
        accounts = [True, False]
        for cash in accounts:
            orders,stock_list = read_orders(cash)
            logger.info(f"read {orders}")
            switch_account(cash)
            trade_list = check_order(orders, stock_list, cash)
            logger.info(f"to trade {trade_list}")
            update_orders(trade_list, cash)
            for stock_info in trade_list:
                trade(stock_info[0], stock_info[1], stock_info[2], stock_info[3])
            sleep(5)
    except Exception as e:
        logger.error(e)
    stop_app("com.tigerbrokers.stock")
run()
# poco("com.tigerbrokers.stock:id/trade_entry_point").children(desc="交易").click()
# poco("com.tigerbrokers.stock:id/text_search_stock_code")[0].click()


