import json
import ctypes
from multiprocessing import Process, Queue, Array
from request_worker import request_worker
from log_worker import log_worker
from info_logger import info_logger
from generate_request_object import generate_request_object
from create_db import create_databases
# define global queues
request_queue = Queue()
response_queue = Queue()

# number of workers to process requests
num_request_workers = 3
num_logging_workers = 1

# shared array to keep track of urls currently being checked
currently_checking_urls = Array(ctypes.c_char_p, num_request_workers)

# initialize database and tables if not already done
create_databases()

# acceptable delay between scheduled time for query and query execution
acceptable_queue_delay = 5  # seconds

# acceptable wait time for website to responsd to request
acceptable_website_response_wait = 5  # seconds


def start_request_workers(n):  # starts n workers to process the queue
    for idx in range(n):
        request_worker_process = Process(target=request_worker,
                                         args=(request_queue,
                                               response_queue,
                                               acceptable_website_response_wait,
                                               currently_checking_urls,
                                               idx))
        request_worker_process.start()


start_request_workers(num_request_workers)

input_file = json.load(open('../urls.json'))

# start processess for each url that periodically generate requests
for input_object in input_file:
    url = input_object["url"]
    interval = input_object["interval"]
    input_url_interval = [url, interval]
    p = Process(target=generate_request_object, 
                args=(input_url_interval,
                      acceptable_queue_delay,
                      request_queue))
    p.start()


def start_log_workers(n):  # starts n log workers
    for x in range(n):
        log_worker_process = Process(target=log_worker, args=(response_queue,))
        log_worker_process.start()


start_log_workers(num_logging_workers)


def start_info_logger_worker(currently_checking_urls):
    info_logger_process = Process(target=info_logger,
                                  args=(currently_checking_urls, ))
    info_logger_process.start()


start_info_logger_worker(currently_checking_urls)
