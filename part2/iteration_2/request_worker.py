import time
import requests
import sys
import random


# worker to make request to the page and push results to response queue
def request_worker(request_queue, 
                   response_queue,  
                   acceptable_website_response_wait,
                   currently_checking_urls,
                   acceptable_queue_delay,
                   idx):
    while True:
        request_object = request_queue.get()
        scheduled_request_time, url, interval = request_object
        currently_checking_urls[idx] = 'url'  # placing url causing issues
        request_received_at = time.time()
        # request was in queue longer than acceptable_queue_delay
        if request_received_at > scheduled_request_time + acceptable_queue_delay:
            fail_code = "stale"
            fail_message = """Request has been in the queue
                              longer than acceptable_queue_delay seconds"""
            response_queue.put([request_received_at,
                                url, 
                                fail_code, 
                                fail_message])
            time.sleep(random.random()*random.randrange(3))  # some randomness
            request_queue.put((scheduled_request_time+interval,
                               url, 
                               interval))
        else:  # request  wasn't stale
            # if request is more than 30 seconds away, put it back in the queue
            if (scheduled_request_time - request_received_at) > 30: 
                request_queue.put((scheduled_request_time,
                                   url,
                                   interval))
                continue
            # wait for scheduled_request_time
            if (scheduled_request_time - request_received_at) > 0: 
                time.sleep(scheduled_request_time - request_received_at)
            request_queue.put((scheduled_request_time+interval,
                               url,
                               interval))
            try:
                request_processing_start_time = time.time()
                r = requests.get(url, timeout=acceptable_website_response_wait)
                url_response_time = time.time() - request_processing_start_time
                status_code = r.status_code
                if status_code == 200:
                    response_size = sys.getsizeof(r.content)
                    response_queue.put([request_processing_start_time,
                                        url, 
                                        response_size, 
                                        url_response_time, 
                                        status_code])        
                else:  
                    # status_code != 200
                    response_queue.put([request_processing_start_time, 
                                        url, 
                                        response_size, 
                                        url_response_time, 
                                        status_code])        
            except requests.exceptions.Timeout:  # Request timed out
                fail_code = "Timeout"
                fail_message = """Target url took longer that 
                                  acceptable_website_response_wait
                                  seconds to respond"""
                response_queue.put([request_processing_start_time,
                                    url,
                                    fail_code,
                                    fail_message])
            except requests.exceptions.ConnectionError:  # Couldn't connect
                fail_code = "ConnectionError" 
                fail_message = """Connection to target url could 
                                  not be established""" 
                response_queue.put([request_processing_start_time,
                                    url,
                                    fail_code,
                                    fail_message])
            except:
                print sys.exc_info()[0]
        currently_checking_urls[idx] = ""
        
