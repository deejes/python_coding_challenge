# takes an array, 
import sqlite3
import time
conn = sqlite3.connect("pf_application_logs.db")
c = conn.cursor()


def drop_table():
    c.execute('drop table if exists url_logs')


def read_all():
    c.execute("select * from url_logs")
    print c.fetchall()

def test_commit():
    c.execute("INSERT INTO url_logs VALUES (?,?,?,?,?)", (str(time.time()), "cnn.com", 123, "123 seconds", "200"))
    

def total_count():
    c.execute("select count(*) from url_logs")    
    result =  c.fetchone()[0]
    return result
    
def top_five_codes():
    c.execute("""
    SELECT http_code, COUNT(*) AS magnitude 
    FROM url_logs 
    GROUP BY http_code
    ORDER BY magnitude DESC
    LIMIT 5
    """)
    print c.fetchall()


def longest_request_last_five_minutes():
    five_mins_ago = (time.time()-300)
    # import pdb; pdb.set_trace()
    c.execute("select max(request_time) from url_logs where timestamp > (?) ", ((time.time()-300),) )
    result = c.fetchone()[0]
    print result

test_commit()

# top_five_codes()
conn.close()

