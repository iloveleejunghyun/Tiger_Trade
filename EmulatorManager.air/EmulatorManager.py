# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *
import Tiger_Trade2
from util import *

auto_setup(__file__)
import threading

#todo start the multiplayer.

dev = connect_device("Windows:///?title_re=夜神多开器.*")

def start_simulator(id):
    clear_selected_simulator()
    touch(Template(r"tpl1623310768453.png", record_pos=(-0.466, -0.149), resolution=(800, 536)))
    touch(Template(r"tpl1623310860880.png", record_pos=(-0.329, -0.266), resolution=(800, 536)))
    sleep(10)
    touch(Template(r"tpl1623310942179.png", record_pos=(-0.399, -0.264), resolution=(800, 536)))
    
    #通过adb devices 查看模拟器是否启动好
    return True


def task1():
    while True:
        title = start_simulator(0)
        res = Tiger_Trade2.run()
    pass

def task2():
    for _ in range(5):
        print("task2")
        sleep(1.5)
    pass

threads = []
t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)

threads.append(t1)
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    
    for t in threads:
        t.join()
    print(f"all over")