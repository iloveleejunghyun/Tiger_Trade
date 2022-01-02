# -*- encoding=utf8 -*-
__author__ = "Administrator"

auto_setup(__file__)
import airtest
from airtest.core.settings import Settings as ST
from util import *
import sys
import os
import logging
logger1=logging.getLogger("airtest")
logger1.setLevel(logging.INFO)
ST.LOG_FILE = "log.txt"
ST.CVSTRATEGY = ['tpl']
ST.THRESHOLD = 0.9

def start_trader():
    import time
    localtime = time.localtime(time.time())

    if not (localtime.tm_hour >= 21):
        logger.info("Can't trade before 21:00")
        return
    import os
    if not os.path.exists("trade.log"):
        logger.info("create trade.log")
        with open("trade.log", 'w'):
            pass
    # 格式化成2016-03-20 11:45:39形式
    date =  time.strftime("%Y-%m-%d", time.localtime()) + '\n'
    with open("trade.log", 'r') as f:
        lines = f.readlines()
        logger.info(lines)
        if len(lines) != 0:
            line = lines[-1]
            
            logger.info(date + ","+line)
            if date == line:
                logger.info("Have traded today")
                return
    logger.info("Start to trade today")
    res = os.system('D: && cd D:\Tiger_Trade\Tiger_Trade2.air && D:\AirtestIDE\AirtestIDE runner D:\Tiger_Trade\Tiger_Trade2.air  --log D:\Tiger_Trade\log')
    logger.info(res)
    with open("trade.log", 'a') as f:
        f.write(date)
    logger.info("Finish trade")
    return

def start_mudi():
    import time
    localtime = time.localtime(time.time())

    if not (localtime.tm_hour >= 21):
        logger.info("Can't mudi before 21:00")
        return
    import os
    if not os.path.exists("mudi.log"):
        logger.info("create mudi.log")
        with open("mudi.log", 'w'):
            pass
    # 格式化成2016-03-20 11:45:39形式
    date =  time.strftime("%Y-%m-%d", time.localtime()) + '\n'
    with open("mudi.log", 'r') as f:
        lines = f.readlines()
        logger.info(lines)
        if len(lines) != 0:
            line = lines[-1]
            
            logger.info(date + ","+line)
            if date == line:
                logger.info("Have mudi today")
                return
    logger.info("Start to mudi today")
    res = os.system('D: && cd D:\mudi\mudi.air && D:\AirtestIDE\AirtestIDE runner D:\mudi\mudi.air  --log D:\mudi\log')
    logger.info(res)
    with open("mudi.log", 'a') as f:
        f.write(date)
    logger.info("Finish mudi")
    return

while True:
    try:
        dev = connect_device("android://127.0.0.1:5037/127.0.0.1:62001?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MINITOUCH")
        break
    except Exception as e:
        logger.info(e)
        logger.info("Try to connect the device after 10s")
        sleep(10)
for i in range(100000):
    try:
        start_trader()
        start_mudi()
        sleep(600)
       
    except Exception as e:
        logger.error("error " + str(e))
        logger.error("需要重启模拟器")
        os.system("shutdown -r -t 120")
        if type(e) is airtest.core.error.AdbShellError:
            
            pass
        pass
    

