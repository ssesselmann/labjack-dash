import sys
from datetime import datetime
import sqlite3 as sql
import time
import u3
import utilities as ut

#-------------------------------------------

def labjack():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("SELECT run_id FROM run_number ORDER BY run_id DESC LIMIT 1")
        lastid = c.fetchone()[0]
        c.execute("DELETE FROM temp_readings")  
    
    state = ut.if_recording(c)

    d = None
    d = u3.U3()
    d.configU3()
    d.getCalibrationData()
    d.configIO(
                EnableCounter0 = True, 
                FIOAnalog = 15,
                TimerCounterPinOffset=4
                )
    d.streamConfig( 
                NumChannels = 6,  
                InternalStreamClockFrequency = 0, 
                Resolution = 3, 
                ScanInterval = 1, 
                PChannels = [0,1,2,3,210,224], 
                NChannels = [31,31,32,31,31,31], 
                ScanFrequency = 4000, 
                )          

    time_stamp = datetime.now()
    d.streamStop()
    while True:
        try:   
            d.streamStart()
            for r in d.streamData(): # I assume r stands for raw data
                if r is not None:   # basically prints an error if there is no raw data

                    time = int(datetime.now().strftime('%s%f'))
                    ain0 = (sum(r['AIN0'])/len(r['AIN0']))
                    ain1 = (sum(r['AIN1'])/len(r['AIN1']))
                    ain2 = (sum(r['AIN2'])/len(r['AIN2']))
                    ain3 = (sum(r['AIN3'])/len(r['AIN3']))
                    ain4 = (r['AIN210'][-1])
                    ain5 = (r['AIN224'][-1])

                    counts32 = ((ain4 << 16) + ain5)

                    if state != ut.if_recording(c):
                        with conn:
                            c.execute("DELETE FROM temp_readings")
                            c.execute("SELECT run_id FROM run_number ORDER BY run_id DESC LIMIT 1")  
                            lastid = c.fetchone()[0]

                    state = ut.if_recording(c)

                    table_name = "dac_readings" if state == True else "temp_readings"

                    with conn:
                        c.execute("SELECT s1, s2 FROM sliderpos")
                        s1, s2 = c.fetchone()
                        
                        c.execute(f"""
                            INSERT INTO  {table_name} (run_id, time, ain0, ain1, ain2, ain3, ain4, s1, s2) 
                            VALUES ({'NULL' if state == False else str(lastid)},{str(time)},{str(ain0)}, {str(ain1)}, {str(ain2)}, {str(ain3)}, {str(ain4)}, {str(s1)},{str(s2)}) 
                            """)    
                    d.writeRegister(5000, s1) # Analogue out slider calibration
                    d.writeRegister(5002, s2) # Analogue out slider calibration

        except Exception as e:
            d.streamStop()
            d.close()
            print('error', e)
            break

#while True:
#labjack()
   

