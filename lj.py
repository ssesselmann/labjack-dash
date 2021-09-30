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
        c.execute("SELECT * FROM preferences ") # Get current preferences
        prefs = c.fetchall()[0]

        max_requests    = prefs[2]
        scan_frequency  = prefs[3]
        factor0         = prefs[5]
        factor1         = prefs[6]
        factor2         = prefs[7]
        factor3         = prefs[8]
        factor4         = prefs[9]
        factor5         = prefs[10]
        factor6         = prefs[11]
        max5            = prefs[25]
        max6            = prefs[26]
    
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
    try:
        d.streamStop()
    except:
        print('error on streamStop')    
    while True:
        try:   
            d.streamStart()
            for r in d.streamData(): # I assume r stands for raw data
                if r is not None:   # basically prints an error if there is no raw data


                    #---------------------------------------------------------------------#
                    #--- The following only runs once when the recording state changes ---#
                    #---------------------------------------------------------------------#
                    if state != ut.if_recording(c):
                        d.streamStop()
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
                        d.streamStart()

                        with conn:
                            c.execute("DELETE FROM temp_readings")
                            c.execute("SELECT run_id FROM run_number ORDER BY run_id DESC LIMIT 1")  
                            lastid = c.fetchone()[0]
                            c.execute("SELECT * FROM preferences ") # Get current preferences
                            prefs = c.fetchall()[0]

                            max_requests    = prefs[2]
                            scan_frequency  = prefs[3]
                            factor0         = prefs[5]
                            factor1         = prefs[6]
                            factor2         = prefs[7]
                            factor3         = prefs[8]
                            factor4         = prefs[9]
                            factor5         = prefs[10]
                            factor6         = prefs[11]

                            max5            = prefs[25]
                            max6            = prefs[26]

                    state = ut.if_recording(c)
                    table_name = "dac_readings" if state == True else "temp_readings"


                    #-----------------------------------------------------------------------------------#
                    #-- The following updates readings with user calibrations                           #
                    #-----------------------------------------------------------------------------------#
                    time = int(datetime.now().strftime('%s%f'))
                    ain0 = (sum(r['AIN0'])/len(r['AIN0']) * factor0)
                    ain1 = (sum(r['AIN1'])/len(r['AIN1']) * factor1)
                    ain2 = (sum(r['AIN2'])/len(r['AIN2']) * factor2)
                    #ain3 = (sum(r['AIN3'])/len(r['AIN3']) * factor3)
                    ain3 = (10**(sum(r['AIN3'])/len(r['AIN3'])-6.125)*1000) # Edwards APGX-H Vacuum Gauge

                    counts32 = ((r['AIN224'][-1] << 16) + r['AIN210'][-1]) * factor4

                    with conn:
                        c.execute("SELECT s1, s2 FROM sliderpos")
                        s1, s2 = c.fetchone()
                        
                        c.execute(f"""
                            INSERT INTO  {table_name} (run_id, time, ain0, ain1, ain2, ain3, ain4, s1, s2) 
                            VALUES ({1 if state == False else str(lastid)},{str(time)},{str(ain0)}, {str(ain1)}, {str(ain2)}, {str(ain3)}, {str(counts32)}, {str(s1)},{str(s2)}) 
                            """)    

                    d.writeRegister(5000, (s1 / factor5)) # Analogue out slider calibration
                    d.writeRegister(5002, (s2 / factor6)) # Analogue out slider calibration

        except Exception as e:
            d.streamStop()
            d.close()
            print('error', e)
            break

#while True:
#labjack()
   

