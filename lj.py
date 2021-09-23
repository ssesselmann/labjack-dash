import sys
import traceback
from datetime import datetime
# import sqlite3 as sql
import time
import u3

#---Sets analog output DAC0 and DAC1 to zero volts on startup

d = None
d = u3.U3()
d.configU3()
d.getCalibrationData()
d.writeRegister(5000,0.0)
d.writeRegister(5002,0.0)
d.close()


#-------------------------------------------

def labjack(scan_frequency, max_requests, s1,s2):

    d = None
    d = u3.U3()
    d.configU3() #  Check if U3 is HV
    d.getCalibrationData()
    rate = 0
    
    try:    # set output voltage based on slider position 
        d.writeRegister(5000, s1) # Analogue out slider calibration
        d.writeRegister(5002, s2) # Analogue out slider calibration

        d.configIO(
            EnableCounter0 = True, 
            FIOAnalog = 15,
            #TimerCounterPinOffset=4
            )

        d.streamConfig( 
            NumChannels = 6,  
            InternalStreamClockFrequency = 0, 
            Resolution = 3, 
            ScanInterval = 1, 
            PChannels = [0,1,2,3,210,224], 
            NChannels = [31,31,31,31,31,31], 
            ScanFrequency = scan_frequency, 
            )
        
        d.streamStart()

        missed = 0
        dataCount = 0
        packetCount = 0
        readings = {"AIN0":[],"AIN1":[],"AIN2":[],"AIN3":[],"AIN210":[],"AIN224":[]}

        for r in d.streamData():
            if len(readings["AIN0"]) >= max_requests:
                d.streamStop()
                d.close()
                break

            if r is not None:
                # Our stop condition
                if dataCount >= max_requests:
                    break

                if r["errors"] != 0:
                    print("Errors counted: %s ; %s" % (r["errors"], datetimd.now()))

                if r["numPackets"] != d.packetsPerRequest:
                    print("----- UNDERFLOW : %s ; %s" %
                          (r["numPackets"], datetime.now()))

                if r["missed"] != 0:
                    missed += r['missed']
                    print("+++ Missed %s" % r["missed"])
                
                for k in readings.keys():
                    readings[k] += r[k]

                dataCount += 1
                packetCount += r['numPackets']

            else:
                print("No data ; %s" % datetimd.now())
                
    except:
        d.streamStop()
        d.close()
        
    now = int(datetime.now().strftime('%s%f'))
    avgs = {'time':now,"s1":s1,"s2":s2 }

    for k in readings.keys():
        if k == 'AIN210':
            avgs[k] = sum(readings[k])  
        else:
            avgs[k] = sum(readings[k])/len(readings[k])     

        lsw = readings['AIN210'][-1]  
        msw = readings['AIN224'][-1]
        counts = ((msw << 16) + lsw)

    avgs.update({'AIN210': counts })

    return avgs



# while True:
#     avgs=labjack(8000,1000,0,0)
#     print(avgs)    