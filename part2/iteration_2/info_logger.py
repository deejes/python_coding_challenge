import sqlite3
import time
from database_metrics_logger import database_metrics_logger

def info_logger(current_checking_urls):
    while True:
        print "urls currently being checked", current_checking_urls[:]
        database_metrics_logger()    
        print "\n\n"
        time.sleep(5)

