#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from queue import Queue
from time import sleep

task_queue, result_queue = Queue(), Queue()

class QueueManager(BaseManager): pass

QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

manager = QueueManager(address=('', 8001), authkey=b'abc')
manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

start_url = 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711'
task.put(start_url)

while True:
    print('master serving ... ')
    sleep(10)
