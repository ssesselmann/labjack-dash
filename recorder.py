import sys
import traceback
from datetime import datetime
import time
import sqlite3 as sql
import lj as lj

#---SQLite Pre recording setup----------------------------------------------------------------------------

def pre_record():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn:
        c.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,               
            heading         TEXT    DEFAULT 'My LabJack U3 Project',    
            max_requests    INTEGER DEFAULT 4000,                        
            scan_frequency  INTEGER DEFAULT 8000,
            interval        INTEGER DEFAULT 500,
            factor0         REAL    DEFAULT 1,
            factor1         REAL    DEFAULT 1,
            factor2         REAL    DEFAULT 1,
            factor3         REAL    DEFAULT 1,
            factor4         REAL    DEFAULT 1,
            factor5         REAL    DEFAULT 1,
            factor6         REAL    DEFAULT 1,
            name0           TEXT    DEFAULT 'AIN0',
            name1           TEXT    DEFAULT 'AIN1',
            name2           TEXT    DEFAULT 'AIN2',
            name3           TEXT    DEFAULT 'AIN3',
            name4           TEXT    DEFAULT 'AIN4',
            name5           TEXT    DEFAULT 'DAC0',
            name6           TEXT    DEFAULT 'DAC1',
            xpoints         INTEGER DEFAULT 100,
            max0            INTEGER DEFAULT 5,
            max1            INTEGER DEFAULT 5,
            max2            INTEGER DEFAULT 5,
            max3            INTEGER DEFAULT 5,
            max4            INTEGER DEFAULT 5,
            max5            INTEGER DEFAULT 10,
            max6            INTEGER DEFAULT 10);
            """)

    with conn:
        c.execute("""
        CREATE TABLE IF NOT EXISTS run_number (
            run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
            time_start      INTEGER NOT NULL,
            time_end        INTEGER);
            """)
        

    with conn:
        c.execute("""
        CREATE TABLE IF NOT EXISTS dac_readings (
            run_id  INTEGER,
            time    INTEGER,
            ain0    REAL,
            ain1    REAL,
            ain2    REAL,
            ain3    REAL,
            ain4    REAL,
            s1      REAL,
            s2      REAL);
            """)

    with conn:
        c.execute("""
            CREATE TABLE IF NOT EXISTS sliderpos (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                s1      REAL,
                s2      REAL);
                """)
#-------------------------------------Checks if table sliderpos is empty and inserts a blank record
    with conn:   
        c.execute("SELECT * FROM sliderpos") 
    if len(c.fetchall()) == 0:
        with conn:
            c.execute("INSERT INTO sliderpos (s1, s2) VALUES (0,0)")
            print('TABLE sliderpos created')        

#-------------------------------------Checks if table run_number is empty and inserts a blank record

    with conn:   
        c.execute("SELECT * FROM run_number") #Check if there are more than one record
    if len(c.fetchall()) == 0:
        with conn:
            c.execute("INSERT INTO run_number (time_start, time_end) VALUES (0,0)")  #Inserting the first record
            print('TABLE run_number created')        

#-------------------------------------Checks if table preferences is empty and inserts a blank record

    with conn:   
        c.execute("SELECT * FROM preferences") 
    if len(c.fetchall()) == 0:
        with conn:
            c.execute("INSERT INTO preferences  (factor0) VALUES (1)")  

        print('TABLE preferences created')

#---------------------------------------------------------------------------------------------------       
    
    #---Checks if the last recording was closed and closes it by updating time_end

    with conn: 
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
    run = c.fetchall()[0]
    lastid = run[0]
    time_end = run[2]

    if time_end == None:
        with conn:
            c.execute(f"UPDATE run_number SET time_end = {int(datetime.now().strftime('%s%f'))} WHERE run_id = {lastid}")
        pass
    return 

#=== Record function from tab 1 ===============================================

def record_avgs(lastid, avgs):

    #print(['recording avgs: ',lastid, avgs])


    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn:
        c.execute("""
        INSERT INTO dac_readings (run_id, time, ain0, ain1, ain2, ain3, ain4, s1, s2) 
            VALUES (?,?,?,?,?,?,?,?,?)
            """, 
            (
                lastid, 
                int(datetime.now().strftime('%s%f')),
                avgs.get('AIN0'),
                avgs.get('AIN1'),
                avgs.get('AIN2'),
                avgs.get('AIN3'),
                avgs.get('AIN210'),
                avgs.get('s1'),
                avgs.get('s2')
                )
            )    
    return
    
#=== End function ===============================================