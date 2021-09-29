import sqlite3 as sql



def if_recording(c):
    c.execute("SELECT time_end FROM run_number ORDER BY run_id DESC LIMIT 1")
    return True if c.fetchone()[0] == None else False