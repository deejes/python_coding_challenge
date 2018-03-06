import sqlite3
import time

def database_metrics_logger():
    conn = sqlite3.connect("pf_application_logs.db")
    c = conn.cursor()
    succesful_queries = succesful_query_count(c)
    failed_queries = failed_query_count(c)
    stale_queries = total_stale_queries(c)
    print "Total requests executed by workers -", succesful_queries + failed_queries
    print "# of stale requests -", stale_queries
    print "# of requests where a response was received-", succesful_queries
    print "5 most frequent Http response codes and their frequency -", top_five_codes(c)
    print "# of requests that timedout or failed to connect -",(failed_queries - stale_queries) 
    print "Longest request in the last five mins took", longest_request_last_five_minutes(c), "seconds"
    conn.close()

def succesful_query_count(cursor):
    cursor.execute("select count(*) from url_logs")    
    return cursor.fetchone()[0]
    
def failed_query_count(cursor):
    cursor.execute("SELECT count(*) FROM error_logs")    
    return cursor.fetchone()[0]    

def longest_request_last_five_minutes(cursor):
    # import pdb; pdb.set_trace()
    cursor.execute("SELECT max(url_response_time) FROM url_logs WHERE timestamp > (?) ", ((time.time()-300),) )
    return cursor.fetchone()[0]

def top_five_codes(cursor):
    cursor.execute("""
    SELECT http_code, COUNT(*) AS magnitude 
    FROM url_logs 
    GROUP BY http_code
    ORDER BY magnitude DESC
    LIMIT 5
    """)
    return cursor.fetchall()

def total_stale_queries(cursor):
    cursor.execute("SELECT count(*) FROM error_logs WHERE fail_code = 'stale'")    
    return cursor.fetchone()[0]
