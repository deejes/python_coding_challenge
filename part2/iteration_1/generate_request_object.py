import time


def generate_request_object(input_array, acceptable_queue_delay, q):
    url = input_array[0] 
    interval = input_array[1]
    while True:
        request_issue_time = time.time()
        expiry_time = request_issue_time + acceptable_queue_delay
        q.put([expiry_time, url])
        time.sleep(interval)

