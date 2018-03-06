import sqlite3
import time

conn = sqlite3.connect("pf_application_logs.db")
c = conn.cursor()


def log_worker(response_queue):
    try:
        while True:
            log_object = response_queue.get()
            if len(log_object) == 5:
                c.execute("INSERT INTO url_logs VALUES (?,?,?,?,?)", tuple(log_object))
                conn.commit()
            else:
                c.execute("INSERT INTO error_logs VALUES (?,?,?,?)", tuple(log_object))
                conn.commit()
    finally:
        conn.close()
