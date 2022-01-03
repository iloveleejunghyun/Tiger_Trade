# -*- encoding=utf8 -*-
#todo 目前只支持一个股票一个挂单（买入/卖出分别一个），因为实际买入卖出价格可能与挂单价不同，不好判断。

__author__ = "Administrator"

from airtest.core.api import *

auto_setup(__file__)


import time, datetime
# from util import * 

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

dev = connect_device("android://127.0.0.1:5037/127.0.0.1:62001?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MINITOUCH")

import logging
# logger=logging.getLogger("airtest")
def initLog(level=logging.DEBUG,filename="pocoLog.txt"):
    '''初始化日志配置
    @param level:设置的日志级别。默认：DEBUG
    @param filename: 日志文件名。默认：当前目录下的pocoLog.txt，也可为绝对路径名
    '''
    logger = logging.getLogger(__name__.split('.')[0])    #日志名为当前包路径project.util.common的
    logger.setLevel(level)
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    streamHandler = logging.StreamHandler(sys.stderr) #输出到控制台
    fileHandler=logging.FileHandler(filename=filename,mode='a',encoding='utf-8',delay=False)
    LOG_FORMAT1='[%(asctime)s] [%(levelname)s] <%(name)s> (%(lineno)d) %(message)s'  
    LOG_FORMAT2='[%(asctime)s] [%(levelname)s] <%(name)s> <%(pathname)s]> (%(lineno)d) %(message)s'
    formatter1 = logging.Formatter(
        fmt=LOG_FORMAT1,
        datefmt='%Y-%m-%d  %H:%M:%S'
    )
    formatter2 = logging.Formatter(
        fmt=LOG_FORMAT2,
        datefmt='%Y-%m-%d  %H:%M:%S'
    )    
    streamHandler.setFormatter(formatter1)
    fileHandler.setFormatter(formatter2)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    #logger.debug('这里是测试用，initlog的logger的debug日志') 
def setPocoLog(name):
    '''设置poco日志配置'''
    pocoLogDIR= os.path.join(ST.PROJECT_ROOT, 'logDir') #poco日志目录
    pocoLogFile=os.path.join(pocoLogDIR,'pocoLog.txt')  #poco日志文件名
    initLog(level=logging.INFO,filename=pocoLogFile)    #poco日志初始化
    logger=logging.getLogger(name)
    return logger
logger = setPocoLog(__name__) #日志方法调用

    

def pclick(id = None, text = None, textMatches = None):
    try:
        if id != None:
            ele = poco(id)
            if ele:
                ele.click()     
                return True
         #   logger.info(f"Didn't Find {id}") 
        elif text != None:
            ele = poco(text = text)
            if ele:
                ele.click()
           #     logger.info(f"Found {text}")
                return True
           # logger.info(f"Didn't Find  {text}")
        else:
            ele = poco(textMatches = textMatches)
            if ele:
                ele.click()
           #     logger.info(f"Found {textMatches}")
                return True
           # logger.info(f"Didn't Find  {textMatches}")
    except Exception as e:
        logger.error(""+e)
    return False

def pwait_click(id = None, text = None, textMatches = None, times=5, disapear=True):
    res = False
    cur_res = False
    for i in range(times):
        cur_res = pclick(id, text, textMatches)
        if cur_res:
            if disapear == False:
                break
            res = cur_res
        else:
            if res: #如果之前找到了就返回。没有找到过就继续找. 这里无法处理多图重复出现之间时间间隔过大的情况
                break
        if i == times-1:
            break
        sleep(1)
    if res:
        if id:
            logger.info(f"Found {id}")
        elif text:
            logger.info(f"Found {text}")
        else:
            logger.info(f"Found {textMatches}")
    else:
        if id:
            logger.info(f"Didn't Find {id}")
        elif text:
            logger.info(f"Didn't Find {text}")
        else:
            logger.info(f"Didn't Find {textMatches}")
    return res

def pwait_until(id = None, text = None, textMatches = None, times = 10):
    if id == None and text == None:
        return True
    for _ in range(times):
        try:
            if id != None:
                if poco(id):
                    logger.info(f"Found {id}")
                    return True
            elif text != None:
                if poco(text = text):
                    logger.info(f"Found {text}")
                    return True
            else:
                if poco(textMatches = textMatches):
                    logger.info(f"Found {textMatches}")
                    return True
        except Exception as e:
            logger.error(""+e)
        sleep(1)
    if id != None:
        logger.info(f"Didn't Find {id}")
    elif text != None:
        logger.info(f"Didn't Find  {text}")
    else:
        logger.info(f"Didn't Find  {textMatches}")
    return False

def screenshot(errmsg):
    name = time.strftime('%Y%m%d %H%M%S') + '-' +errmsg
    import os
    name = f'{os.getcwd()}\\errscreen\\{name}.png'
    print(name)
    snapshot(filename=name,msg='massage')
    
def back_to_main():
    pwait_click("com.tigerbrokers.stock:id/btn_cancel")

    #advertisement
    pwait_click(text="关闭弹框",times=1)

    for _ in range(5):
        if not pwait_click("com.tigerbrokers.stock:id/text_main_bottom_market",times=1):
            pwait_click(text="关闭弹框",times=1)
            keyevent("KEYCODE_BACK")
            sleep(2)
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
    
    pwait_click("com.tigerbrokers.stock:id/text_main_bottom_trade")

    pwait_click("com.tigerbrokers.stock:id/fab_text_action_left")
    pwait_until("com.tigerbrokers.stock:id/account_title")
    eles = poco("com.tigerbrokers.stock:id/account_title")
#     logger.info(len(eles))
    if cash == True:
        eles[0].click()
#         pwait_click(text="综合账户")
#         pwait_click("com.tigerbrokers.stock:id/stock_trade_entry_deal")
        logger.info("Switch to cash account")
        input_trade_pass()
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
        
# check_update()
import os
def run():
#     print(os.getcwd())
#     pclick(text="综合账户")
##    switch_account(True)
#     switch_account(False)
    try:
        logger.info("start to trade")
        stop_app("com.tigerbrokers.stock")
        sleep(5)
        start_app("com.tigerbrokers.stock")
        sleep(10)
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

