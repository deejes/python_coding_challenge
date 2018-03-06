import json
import time
import ctypes
import random
from multiprocessing import Process, Queue, Array
from create_db import create_databases
from request_worker import request_worker
from log_worker import log_worker
from info_logger import info_logger
from managed_priority_queue import shared_priority_queue
# number of workers to process requests
num_request_workers = 3
num_logging_workers = 1
# acceptable delay between scheduled time for query and query execution
acceptable_queue_delay = 5  # seconds

# acceptable wait time for website to responsd to request
acceptable_website_response_wait = 5  # seconds

# initialize database and tables if not already done
create_databases()

# create shared memeory datastructures 
request_queue = shared_priority_queue()
response_queue = Queue()
currently_checking_urls = Array(ctypes.c_char_p, num_request_workers)

# staggered initial insert into request_queue 
input_file = json.load(open('../urls.json'))
for input_object in input_file:
    url = input_object["url"]
    interval = input_object["interval"]
    time.sleep(random.random()+random.randrange(2))  # causes some stale reqs
    request_queue.put((time.time(), url, interval))


def start_request_workers(n):  # starts n workers to process the queue
    for idx in range(n):
        request_worker_process = Process(target=request_worker,
                                         args=(request_queue,
                                               response_queue,
                                               acceptable_website_response_wait,
                                               currently_checking_urls,
                                               acceptable_queue_delay,
                                               idx))
        request_worker_process.start()


start_request_workers(num_request_workers)


def start_log_workers(n):
    for _ in range(n):
        log_worker_process = Process(target=log_worker, 
                                     args=(response_queue, ))
        log_worker_process.start()


start_log_workers(num_logging_workers)


def start_info_logger_worker(currently_checking_urls):
    info_logger_process = Process(target=info_logger, 
                                  args=(currently_checking_urls,))
    info_logger_process.start()


start_info_logger_worker(currently_checking_urls)


# Sub optimal way of dealing with issue arising out of shared priority queue
while True:
    time.sleep(100000)
