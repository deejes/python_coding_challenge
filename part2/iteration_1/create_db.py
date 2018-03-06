import sqlite3


def create_databases():
        conn = sqlite3.connect("pf_application_logs.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS url_logs (
                        timestamp real,
                        url text,
                        body_size integer,
                        url_response_time real,
                        http_code integer
                        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS error_logs (
                        timestamp real,
                        url text,
                        fail_code text,
                       fail_code_description text
                        )""")
        conn.commit()
        conn.close()
