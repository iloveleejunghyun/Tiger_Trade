# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *

auto_setup(__file__)


import time, datetime

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

def wait_click(temp_list):
    if type(temp_list) is not list:
        temp_list = [temp_list]
    while True:
        find = False
        for temp in temp_list:
            pos =  exists(temp)
            if pos:
                try:
                    touch(pos)
                    find = True
                    sleep(2)
                except:
                    pass
        if find == False:
            return
        
def start_tiger():
    start_app("com.tigerbrokers.stock")
    
# def close_tiger():
#     close_app("com.tigerbrokers.stock")
    
def back_to_main():
    #advertisement
    ele = poco(desc="关闭弹框")
    if ele:
        ele.click()


    while True:
            ele = poco("com.tigerbrokers.stock:id/text_main_bottom_market")
            if ele:
                ele.click()
                return
            else:
                keyevent("KEYCODE_BACK")
                sleep(2)
def check_order(stock_list, cash=False):
    back_to_main()
    poco(text="交易").click()


    poco(text="订单").click()

    #已成交
    poco(text="已成交").click()

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

    # print(record_arr)
    new_list = []
    for dic in record_arr:
        if time_ok(dic['date']):
            if (dic['code'], dic['price'], dic['count'], dic['orientation']) in stock_list:
                print('traded', dic)
                stock_list.remove((dic['code'], dic['price'], dic['count'], dic['orientation']))
                append_history_orders([(dic['code'], dic['price'], dic['count'], dic['orientation'], dic['date'])], cash)
    return stock_list

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

def switch_account(cash=False):
    back_to_main()
    poco(text="交易").click()
    
    poco("com.tigerbrokers.stock:id/fab_text_action_left").click()
    
    eles = poco("com.tigerbrokers.stock:id/account_title")
    print(len(eles))
    if cash == True:
        eles[0].click()
        poco("com.tigerbrokers.stock:id/stock_trade_entry_deal").click()
        input_trade_pass()
    else:
        eles[1].click()
        
def trade(stock_code, stock_price, stock_count, direction):
    back_to_main()
    poco(text="行情").click()

    #search
    poco("com.tigerbrokers.stock:id/fab_image_btn_right_2").click()
    poco("com.tigerbrokers.stock:id/edit_ab_search_stock").set_text(stock_code)
    sleep(10)
    poco("com.tigerbrokers.stock:id/text_search_stock_code")[0].click()
    poco("com.tigerbrokers.stock:id/text_tabbar_trade").click()

    #buy or sell
    if direction == '买入':
        poco("com.tigerbrokers.stock:id/bg_image_buy_in").click()
    else:
        poco("com.tigerbrokers.stock:id/bg_image_sell").click()

    # edit the price and amount
    eles = poco("com.tigerbrokers.stock:id/edit_number")
    eles[0].set_text(str(stock_price))
    eles[1].set_text(str(stock_count))

    poco("com.tigerbrokers.stock:id/btn_place_order_submit").click()

    
def input_trade_pass():
    keyevent("KEYCODE_3")
    keyevent("KEYCODE_2")
    keyevent("KEYCODE_1")
    keyevent("KEYCODE_6")
    keyevent("KEYCODE_5")
    keyevent("KEYCODE_4")



# res = poco("com.tigerbrokers.stock:id/text_item_order_history_code")
# print(res[0].get_text(), res[1].get_text(), res[2].get_text())
# start_tiger()
# sleep(10)
def run():
    start_app("com.tigerbrokers.stock")
    sleep(10)
    cash = True
    orders = read_orders(cash)
    print("read", orders)
    switch_account(cash)
    trade_list = check_order(orders, cash)
    print("to trade",trade_list)
    update_orders(trade_list, cash)
    for stock_info in trade_list:
        trade(stock_info[0], stock_info[1], stock_info[2], stock_info[3])
    sleep(5)
    stop_app("com.tigerbrokers.stock")
run()
# poco("com.tigerbrokers.stock:id/trade_entry_point").children(desc="交易").click()
# poco("com.tigerbrokers.stock:id/text_search_stock_code")[0].click()