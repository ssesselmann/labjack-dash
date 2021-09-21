import dash
#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from server import app
import dash_daq as daq
import tkinter as tk
import recorder as rec
import time
import sqlite3 as sql
from datetime import datetime
import lj as lj

#+++ START PAGE RENDERING +++++++++++++++++++++++++++++++++++++++++++++++++++++++

def tab1():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    c.execute("SELECT * FROM preferences ") # Get current preferences
    row = c.fetchall()[0]

    heading         = row[1]
    max_requests    = row[2]
    scan_frequency  = row[3]
    interval        = row[4]

    factor0         = row[5]
    factor1         = row[6]
    factor2         = row[7]
    factor3         = row[8]
    factor4         = row[9]
    factor5         = row[10]
    factor6         = row[11]
    
    name0           = row[12]
    name1           = row[13]
    name2           = row[14]
    name3           = row[15]
    name4           = row[16]
    name5           = row[17]
    name6           = row[18]

    s1 = 0
    s2 = 0

    p0 = 0 * factor5 
    p1 = 1 * factor5
    p2 = 2 * factor5
    p3 = 3 * factor5
    p4 = 4 * factor5
    p5 = 5 * factor5

    q0 = 0 * factor6
    q1 = 1 * factor6
    q2 = 2 * factor6
    q3 = 3 * factor6
    q4 = 4 * factor6
    q5 = 5 * factor6
    

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
                    html.Button('Record', id='start', n_clicks=0, style={'backgroundColor':'lightgreen', 'width':'100px'}),
                    html.Div(id='output',style={'color':'white', 'height':'15px'}), 
                    html.Div(id='output2',style={'color':'white', 'height':'15px'}), 
                        ]
                ),

        html.Div(
            style={
                'width':'80%',
                'color':'yellow', 
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
                'color':'yellow', 
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
                max= 5 * factor5,
                value=0,
                step=0.1,
                updatemode='drag',
                marks={
                    p0:str("{:.1f}".format(p0)),
                    p1:str("{:.1f}".format(p1)),
                    p2:str("{:.1f}".format(p2)),
                    p3:str("{:.1f}".format(p3)),
                    p4:str("{:.1f}".format(p4)),
                    p5:str("{:.1f}".format(p5)),
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
                },

                # children=[daq.BooleanSwitch(
                # id='switch', 
                # on=False,
                # color="#74FF33",),

                # html.Div(
                #     id='kill-switch-output'
                #     )]
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
                    max= 5 * factor6,
                    step=0.1,
                    value=0,
                    updatemode='drag',
                    marks={
                        q0:str("{:.1f}".format(q0)),
                        q1:str("{:.1f}".format(q1)),
                        q2:str("{:.1f}".format(q2)),
                        q3:str("{:.1f}".format(q3)),
                        q4:str("{:.1f}".format(q4)),
                        q5:str("{:.1f}".format(q5)),
                        },
                ),
        
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
                max=5*factor0,
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
                max=5*factor1,
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
                color='yellow',
                showCurrentValue=True,
                units= name2,
                value= 0,
                label= name2,
                max=5*factor2,
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
                logarithmic=True,
                showCurrentValue=True,
                units= name3,
                value=10,
                label= name3,
                max=5*factor3,
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
                showCurrentValue=True,
                units= name4,
                value=0,
                label= name4,
                max=5*factor4,
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

#+++ This callback only sets the recording status ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.callback(
    Output('output', 'children'),
    Input('start', 'n_clicks'))

def record_status_text(n1):

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn: 
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")

    row = c.fetchone()
    lastid = row[0]
    time_end = row[2]

    status = 'RECORDING' if ((n1 != 0) and (len(row) == 0 or time_end is not None)) else 'NOT RECORDING'
    return str(status)

# ------------Starts and Stops recording--------------------------------------    

@app.callback(
    Output('output2', 'children'),
    Input('start', 'n_clicks'),
    [State('s1', 'value'), State('s2','value')])

def start_stop_record(n,s1,s2):
    if n == 0:
        return 

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn: 
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")

    row = c.fetchone()

    lastid = row[0]
    time_end = row[2]

    status = 'NOT RECORDING' if (len(row) == 0 or time_end is not None) else 'RECORDING'

    if n > 0 and status == 'NOT RECORDING': #There is no active recording and so starting a new one
        
        with conn:
            c.execute("SELECT * FROM preferences ")

            row = c.fetchall()[0]

            heading         = row[1]
            max_requests    = row[2]
            scan_frequency  = row[3]
            interval        = row[4]

            factor0         = row[5]
            factor1         = row[6]
            factor2         = row[7]
            factor3         = row[8]
            factor4         = row[9]
            factor5         = row[10]
            factor6         = row[11]
            
        #     name0           = row[12]
        #     name1           = row[13]
        #     name2           = row[14]
        #     name3           = row[15]
        #     name4           = row[16]
        #     name5           = row[17]
        #     name6           = row[18]

        now = int(datetime.now().strftime('%s%f'))

        with conn:  # Inserts all fields except time_end
            c.execute(f"INSERT INTO run_number (time_start) VALUES ({now}) ")
                

            
        # with conn:  # Inserts all fields except time_end
        #     c.execute("""
        #         INSERT INTO run_number 
        #         (time_start, heading, max_requests, scan_frequency, interval, factor0, factor1, factor2, factor3, factor4, factor5, factor6, name0, name1, name2, name3, name4, name5, name6) 
        #         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        #         (int(datetime.now().strftime('%s%f')),heading,max_requests,scan_frequency,interval,factor0,factor1,factor2,factor3,factor4, factor5, factor6, name0, name1, name2, name3, name4, name5, name6))

        # with conn: 
        #     c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
        #     row = c.fetchone()
        #     lastid = row[0]



#---- ENDLESS LOOP ------------------------------------------------------------------------
      
        while True:

            with conn: 
                c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
                row = c.fetchone()
                lastid = row[0]
                time_end = row[2]

            closed = True if time_end is not None else False

            if closed == True:
                break

            with conn:
                c.execute("SELECT * FROM sliderpos WHERE id = 1")
                row = c.fetchall()[0]   
                s1 = row[1]
                s2 = row[2] 

            avgs = lj.labjack(scan_frequency, max_requests, s1, s2)

            avgs.update({
                'AIN0':(avgs.get('AIN0') * factor0),
                'AIN1':(avgs.get('AIN1') * factor1),
                'AIN2':(avgs.get('AIN2') * factor2),
                'AIN3':(10**(avgs['AIN3']-6.125)*10000000),
                'AIN4':(avgs.get('AIN210')), # net counts
                's1':(s1),
                's2':(s2)
            })

            rec.record_avgs(lastid,avgs)   # Writes  data to disk

#--- ENDLESS LOOP STOP ---------------------------------------------------------------------------    

    else:   #   There is an open detected and so closing the opened run
        
        with conn: 
            c.execute(f"UPDATE run_number SET time_end = {str(int(datetime.now().strftime('%s%f')))} WHERE run_id = {str(row[0])} ")
        
        print(f'Run_id : {str(row[0])} has been closed')        

    return f"(Last recording {lastid})"

#+++ END OF RECORD LOGIC - START INTERVAL PAGE REFRESH CALLBACK +++++++++++++++++++++++++++++++++++++++++++++
    
@app.callback(
    Output('ain0','value'), 
    Output('ain1','value'),
    Output('ain2','value'),
    Output('ain3','value'),
    Output('ain4','value'),
    Output('clock', 'children'),
    Output('s1_output', 'children'),
    Output('s2_output', 'children'),
    Input('interval_gauges','n_intervals'),
    [State('s1', 'value'), State('s2','value')]
    )

def refresh_page(n, s1, s2):

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()


    with conn:
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
        row = c.fetchall()[0]
        lastid      = row[0]
        time_start  = row[1]
        time_end    = row[2]

    with conn:
        c.execute("SELECT * FROM preferences")
        row = c.fetchall()[0]

        max_requests    = row[2]
        scan_frequency  = row[3]

        factor0 = row[5]
        factor1 = row[6]
        factor2 = row[7]
        factor3 = row[8]
        factor4 = row[9]
        factor5 = row[10]
        factor6 = row[11]



    recording = False if (len(row) == 0 or time_end is not None) else True

    if recording == True:

        with conn:
            c.execute(f"""
                    SELECT
                        run_id,     
                        TIME,
                        ain0,
                        ain1,
                        ain2,
                        ain3,
                        AVG(ain4) OVER (
                            ORDER BY
                                TIME ROWS BETWEEN 10 PRECEDING
                                AND 0 FOLLOWING
                        ) * {scan_frequency} / {max_requests} AS ain4,
                        s1,
                        s2
                    FROM
                        dac_readings
                    WHERE
                        run_id = '{lastid}'
                    ORDER BY
                        TIME DESC
                    LIMIT
                        1
                        """)

        row = c.fetchone()

        try:

            avgs = dict([
                ('AIN0',row[2]),
                ('AIN1',row[3]),
                ('AIN2',row[4]),
                ('AIN3',row[5]),
                ('AIN4',row[6]),
                ('s1',row[7]),
                ('s2',row[8])
                ])

        except:
            print('* SELECT failed *')



    else:

        try:
            avgs = lj.labjack(scan_frequency, max_requests, s1/factor5, s2/factor6) # Null handled exception here means it is biting it's tail
        except:
            print('Failed to connect with LabJack')


        avgs.update({
            'AIN0':(avgs.get('AIN0') * factor0),
            'AIN1':(avgs.get('AIN1') * factor1),
            'AIN2':(avgs.get('AIN2') * factor2),
            'AIN3':(10**(avgs['AIN3']-6.125)*10000000),
            'AIN4':(avgs.get('AIN210')), # net counts
            's1':(avgs.get('s1') * factor5),
            's2':(avgs.get('s2') * factor6)
            }) 

    now = datetime.now()
    clock = now.strftime("%H:%M:%S")

    #print(avgs['AIN4'])
    return [avgs['AIN0'],avgs['AIN1'],avgs['AIN2'],avgs['AIN3'],avgs['AIN4'],clock,avgs['s1'],avgs['s2']]               # Outputs the data to apps



#--- UPDATE SLIDERPOS TABLE EVERY TIME SLIDER MOVES ------------------------------------------------------

@app.callback(
    Output('slipper', 'value'),
    [Input('s1', 'value'), Input('s2','value')]
    )
    
def update_sliderpos(s1,s2):

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn:
        c.execute(f"""UPDATE sliderpos SET s1 == {s1},s2 == {s2} """)

#--------------------------------------------------------------------------------------------