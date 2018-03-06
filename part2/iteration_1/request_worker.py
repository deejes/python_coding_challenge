import time
import requests
import sys


# worker to make request to the page and push results to response queue
def request_worker(request_queue, 
                   response_queue, 
                   acceptable_website_response_wait, 
                   currently_checking_urls,
                   idx):
    while True:
        request_object = request_queue.get()
        request_expiry_time, url = request_object
        request_processing_start_time = time.time()
        # assigning actual url causes errors. Leaving "url" as placeholder.
        currently_checking_urls[idx] = "url"  
        if request_processing_start_time > request_expiry_time:  # stale
            fail_code = "stale"
            fail_message = """Request has been in the queue 
                              longer than acceptable_queue_delay seconds"""
            response_queue.put([request_processing_start_time,
                                url, 
                                fail_code,
                                fail_message])
        else:
            try:
                request_sent_time = time.time()
                r = requests.get(url, timeout=acceptable_website_response_wait)
                url_response_time = time.time()-request_sent_time
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
                # print fail_message,url
                response_queue.put([request_processing_start_time,
                                    url,
                                    fail_code,
                                    fail_message])
            except requests.exceptions.ConnectionError:
                fail_code = "ConnectionError" 
                fail_message = """Connection to target 
                                  url could not be established""" 
                # print fail_message,url
                response_queue.put([request_processing_start_time,
                                    url,
                                    fail_code,
                                    fail_message])
        currently_checking_urls[idx] = ""
        
