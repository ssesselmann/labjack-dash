import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from server import app
import dash_daq as daq
import utilities as ut
import tkinter as tk
import recorder as rec
import time
import sqlite3 as sql
from datetime import datetime
from itertools import islice



avgs = []

#+++ START PAGE RENDERING +++++++++++++++++++++++++++++++++++++++++++++++++++++++

def tab1():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    c.execute("SELECT * FROM preferences ") # Get current preferences
    prefs = c.fetchall()[0]

    heading         = prefs[1]
    max_requests    = prefs[2]
    scan_frequency  = prefs[3]
    interval        = prefs[4]

    factor0         = prefs[5]
    factor1         = prefs[6]
    factor2         = prefs[7]
    factor3         = prefs[8]
    factor4         = prefs[9]
    factor5         = prefs[10]
    factor6         = prefs[11]
    
    name0           = prefs[12]
    name1           = prefs[13]
    name2           = prefs[14]
    name3           = prefs[15]
    name4           = prefs[16]
    name5           = prefs[17]
    name6           = prefs[18]

    max0            = prefs[20]
    max1            = prefs[21]
    max2            = prefs[22]
    max3            = prefs[23]
    max4            = prefs[24]
    max5            = prefs[25]
    max6            = prefs[26]

    s1 = 0
    s2 = 0

    p0  = max5/10*0
    p1  = max5/10*1
    p2  = max5/10*2
    p3  = max5/10*3
    p4  = max5/10*4
    p5  = max5/10*5
    p6  = max5/10*6
    p7  = max5/10*7
    p8  = max5/10*8
    p9  = max5/10*9
    p10 = max5/10*10


    q0 = max6/10*0
    q1 = max6/10*1
    q2 = max6/10*2
    q3 = max6/10*3
    q4 = max6/10*4
    q5 = max6/10*5
    q6 = max6/10*6
    q7 = max6/10*7
    q8 = max6/10*8
    q9 = max6/10*9
    q10 =max6/10*10

    with conn:
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
        run = c.fetchone()
        time_end = run[2]

        if time_end == None:
            state = True
        else: state = False    
    
    with conn:
        c.execute("SELECT * FROM sliderpos")
        sliderpos = c.fetchone()

        pos1 = sliderpos[1]
        pos2 = sliderpos[2]

    tab1 = html.Div([   # Page refresh
        dcc.Interval(
            id='interval_gauges',
            interval= interval, 
            n_intervals=0,
            disabled=False 
            ),

        html.Div([
            html.P(str(heading))], # Page heading
            style={
                'width':'80%', 
                'height':80, 
                'marginTop':0,
                'textAlign':'center',
                'fontSize':30,
                'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                }),

#---Heading ----------------------------------------------------------------------------------------------------        
        html.Div(
            style={
                'width':'20%', 
                'height':30, 
                'marginTop':0,
                'textAlign':'center', 
                'fontSize':30,
                'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                }),
#---Record switch---------------------------------------------------------------------------------------------

        html.Div(
            style={
                'color':'white', 
                'width':'20%', 
                'backgroundColor':'black', 
                'float':'right',
                'height':'60px',
                'textAlign':'center'
                },

                children=[ 
                    daq.BooleanSwitch(id='start', on = state, style={'backgroundColor':'black','width':'100px'}),
                    html.Div(id='output_status',style={'color':'red', 'height':'15px', 'textAlign':'left', 'padding':'5px'}), 
                    html.Div(id='output_lastid',style={'color':'white', 'height':'15px', 'textAlign':'left', 'padding':'5px'}), 
                        ]
                ),

        html.Div(
            style={
                'width':'80%',
                'textAlign':'center',
                'color':'orange', 
                'backgroundColor':'black',
                'height':'50px',
                'float':'left'
                }),
            
        html.Div( 
            id='stop_output',
            style={ 'marginTop': 0,
                'height':'40px',
                'width':'20%', 
                'textAlign':'center',
                'color':'orange', 
                'backgroundColor':'black',
                'float':'left'
                }),
     
#---Voltage Slider--------------------------------------
        html.Div(
            style={
                'marginTop': 0,
                'width':'80%',
                'backgroundColor':'black',
                'float':'left',
                'height':'100px',
                'fontWeight':'bold'
                },
                children= [dcc.Slider(
                id='s1',
                min=0,
                max= max5,
                value=pos1,
                step=0.1,
                updatemode='drag',
                marks={
                    int(p0):'{}'.format(int(p0)),
                    int(p1):'{}'.format(int(p1)),
                    int(p2):'{}'.format(int(p2)),
                    int(p3):'{}'.format(int(p3)),
                    int(p4):'{}'.format(str(p4)),
                    int(p5):'{}'.format(str(p5)),
                    int(p6):'{}'.format(str(p6)),
                    int(p7):'{}'.format(str(p7)),
                    int(p8):'{}'.format(str(p8)),
                    int(p9):'{}'.format(str(p9)),
                    int(p10):'{}'.format(str(p10)),
                    },),

                html.Div([ html.Div(id='s1_output'),(name5)], 
                style={ 'marginTop': 10, 'color':'white',  'textAlign':'center', 'fontSize':'16px'}),
            
                ]
        ),

#---Kill switch -----------------------------------------------------        

        html.Div(id='dummy2',
            style={
                'width':'20%', 
                'backgroundColor':'black', 
                'float':'right',
                'height':'50px'
                }
                ),

        html.Div(
            style={ 
            'marginTop': 0,
            'height':'50px',
            'width':'20%', 
            'textAlign':'center',
            'color':'white',
            'backgroundColor':'black',
            'float':'left'
            }),

#---Pressure Slider--------------------------------------

        html.Div( style={
                'width':'80%', 
                'backgroundColor':'black', 
                'float':'left',
                'height':'100px',
                'fontWeight':'bold'
                },

                children= [dcc.Slider(
                    id='s2',
                    min=0,
                    max= max6,
                    step=0.1,
                    value=pos2,
                    updatemode='drag',
                    marks={
                        int(q0):'{}'.format(int(q0)),
                        int(q1):'{}'.format(int(q1)),
                        int(q2):'{}'.format(int(q2)),
                        int(q3):'{}'.format(int(q3)),
                        int(q4):'{}'.format(str(q4)),
                        int(q5):'{}'.format(str(q5)),
                        int(q6):'{}'.format(str(q6)),
                        int(q7):'{}'.format(str(q7)),
                        int(q8):'{}'.format(str(q8)),
                        int(q9):'{}'.format(str(q9)),
                        int(q10):'{}'.format(str(q10)),
                        },),
        
                html.Div([ html.Div(id='s2_output'),(name6)], 
                style={ 'marginTop': 10, 'color':'white',  'textAlign':'center', 'fontSize':'16px'}),   
        ]),
        
        html.Div([    
            
        html.Div([ html.P(id='clock')],
            style={
                'fontSize':20,
                'marginTop': 0,
                'height':'100px',
                'width':'20%', 
                'textAlign':'center',
                'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                }),

        
#---Channel Reading 0 ----------------------------------------------------------        
        
        html.Div([
            daq.Gauge(
                id='ain0',
                size=200,
                color='red',
                showCurrentValue=True,
                units= name0,
                value= 0,
                label= name0,
                max= max0,
                min=0,
            ),
        
            ],
            style={
                'width':'20%', 
                'height':300, 
                'marginTop':0,
                'textAlign':'center', 
                'fontSize':30,'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                },
            ),

#---Channel Reading 1 ------------------------------------------------------------
            
        html.Div([
            daq.Gauge(
                id='ain1',
                size=200,
                color='green',
                showCurrentValue=True,
                units= name1,
                value= 0,
                label= name1,
                max= max1,
                min=0,
            ),

            ],
            style={
                'width':'20%', 
                'height':300, 
                'marginTop':0,
                'textAlign':'center', 
                'fontSize':30,'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                },
            ),

#---Channel Reading 2 ------------------------------------------------------------        
        
                html.Div([
            daq.Gauge(
                id='ain2',
                size=200,
                color='orange',
                showCurrentValue=True,
                units= name2,
                value= 0,
                label= name2,
                max= max2,
                min=0,
            ),

            ],
            style={
                'width':'20%', 
                'height':300, 
                'marginTop':0,
                'textAlign':'center', 
                'fontSize':30,'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                },
            ),

#---Channel Reading 3 -------------------------------------------------------------
        
        html.Div([
            daq.Gauge(
                id='ain3',
                size=200,
                color='blue',
                logarithmic=False,
                showCurrentValue=True,
                units= name3,
                value=0,
                label= name3,
                max= max3,
                min=0,
               
            )],
            style={
                'width':'20%', 
                'height':300, 
                'marginTop':0,
                'textAlign':'center', 
                'fontSize':30,'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                },
            ),

#---Channel Reading 4 --------------------------------------------------------------    
        
        html.Div([
            daq.Gauge(
                id='ain4',
                size=200,
                color='purple',
                logarithmic=False,
                showCurrentValue=True,
                units= name4,
                value=0,
                label= name4,
                max= max4,
                min=0,
               
            )],
            style={
                'width':'20%', 
                'height':300, 
                'marginTop':0,
                'textAlign':'center', 
                'fontSize':30,'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                },
            )
        ]),
        html.Div(children='Bee Research Pty Ltd 2021',
            style={
                'width':'100%', 
                'height':200, 
                'marginTop':0,
                'textAlign':'center', 
                'fontSize':12,
                'color':'white', 
                'backgroundColor':'black',
                'float':'left'
                }),
        html.Div(id='slipper')


    ])

    return tab1

#--- END OF PAGE RENDERING --------------------------------------------------------------------------


@app.callback(
    Output('output_status', 'children'),
    Output('ain0','value'), 
    Output('ain1','value'),
    Output('ain2','value'),
    Output('ain3','value'),
    Output('ain4','value'),
    Output('clock', 'children'),
    Output('s1_output', 'children'),
    Output('s2_output', 'children'),
    Input('interval_gauges','n_intervals'),
    [State('start', 'on'), State('s1', 'value'), State('s2','value')]
    )

def record_status_text(on, n, s1, s2):

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn: 
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
        run = c.fetchone()
        lastid      = run[0]
        time_end    = run[2]

    status = 'RECORDING: '+str(lastid) if (on == True) else 'NOT RECORDING'

    table = 'dac_readings' if (on == True) else 'temp_readings'

    with conn:
        c.execute("SELECT * FROM preferences")
        prefs = c.fetchone()
        max_requests    = prefs[2]
        scan_frequency  = prefs[3]
        factor0         = prefs[5]
        factor1         = prefs[6]
        factor2         = prefs[7]
        factor3         = prefs[8]
        factor4         = prefs[9]
        factor5         = prefs[10]
        factor6         = prefs[11]

        max0            = prefs[20]
        max1            = prefs[21]
        max2            = prefs[22]
        max3            = prefs[23]
        max4            = prefs[24]
        max5            = prefs[25]
        max6            = prefs[26]

    state = ut.if_recording(c)
    table_name = "dac_readings" if state == True else "temp_readings"    

    with conn:
        c.execute(f"SELECT ain0, ain1, ain2, ain3 FROM {table_name} ORDER BY time DESC LIMIT 1")
        readings = c.fetchone()
        c.execute(f"SELECT (MAX(ain4) - MIN(ain4))/5 AS cps FROM {table_name} WHERE time > (SELECT MAX(time) FROM {table_name}) -5000000")
        cps = c.fetchone()[0]

    

    avgs = {}
    avgs['AIN0'] = readings[0]
    avgs['AIN1'] = readings[1]
    avgs['AIN2'] = readings[2]
    avgs['AIN3'] = readings[3]
  
   

    avgs.update({
        'AIN0':(avgs.get('AIN0') / factor0 * max0),
        'AIN1':(avgs.get('AIN1') / factor1 * max1),
        'AIN2':(avgs.get('AIN2') / factor2 * max2),
       #'AIN3':(avgs.get('AIN3') / factor3 * max3),
        'AIN3':(10**(avgs['AIN3']-6.125) * 1000),   # Edwards APGX-H Vacuum Gauge
        'AIN4':(cps), # net counts
        's1':(s1),
        's2':(s2)
        })

    #print(avgs)

    if n == True and time_end != None:
        now = int(datetime.now().strftime('%s%f'))

        with conn:  
            c.execute(f"INSERT INTO run_number (time_start) VALUES ({now}) ")  
    
    if n == False and time_end == None: 
        now = int(datetime.now().strftime('%s%f'))
        with conn:  
            c.execute(f"UPDATE run_number SET time_end = '{now}' WHERE run_id = '{lastid}' ")
        with conn:
            c.execute("SELECT * from run_number ORDER BY run_id DESC LIMIT 1")
            run = c.fetchone()
            time_end = run[2]

    now = datetime.now()
    clock = now.strftime("%H:%M:%S")
      

    return [status, avgs['AIN0'],avgs['AIN1'],avgs['AIN2'],avgs['AIN3'],avgs['AIN4'],clock,avgs['s1'],avgs['s2']]

#--- UPDATE SLIDERPOS TABLE EVERY TIME SLIDER MOVES ------------------------------------------------------

@app.callback(
    Output('slipper', 'value'),
    [Input('s1', 'value'), Input('s2','value')]
    )
    
def update_sliderpos(s1,s2):

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute(f"UPDATE sliderpos SET s1 == {s1},s2 == {s2} ")

#--------------------------------------------------------------------------------------------