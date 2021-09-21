import dash
#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
import time
from datetime import datetime
from dash.dependencies import Input, Output, State
from server import app
import sqlite3 as sql
import plotly.graph_objs as go
import sqlite3 as sql
import recorder as rec
import lj as lj
import math
import numpy as np

#---------------- Page Layout ------------------------------------------------------

def tab3():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn:
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")

        row = c.fetchall()

        interval = row[0][6]
        name0   = row[0][14]
        name1   = row[0][15]
        name2   = row[0][16]
        name3   = row[0][17]
        name4   = row[0][18]
        name5   = row[0][19]

    tab3 = html.Div([ dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': name0, 'value': 'AIN0'},
            {'label': name1, 'value': 'AIN1'},
            {'label': name2, 'value': 'AIN2'},
            {'label': name3, 'value': 'AIN3'},
            {'label': name4, 'value': 'AIN4'}
            ],style={'textAlign':'center'},
        
        value='AIN0', #default value

            ),

        html.Div(id='dd-output-container'),

        dcc.Interval(
        id='interval',
        interval=interval, 
        n_intervals=0),


        html.Div([ 
            dcc.Graph( id='fig' ),
            ],
            style = {'width':'100%',"border":"3px gray solid",'display':'inline-block'}
            )         
            ],
            style = {'color':'black'},



            )

        
    
    return tab3

#---------------- END PAGE LAYOUT ------------------------------------------------------    

@app.callback( 
    Output('fig','figure'),
    [Input('interval','n_intervals')],
    State('dropdown', 'value')
    )

def interval(n,value):

    i = None

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    # Get position of sliders
    with conn:
        c.execute("SELECT * FROM sliderpos WHERE id = 1")
    row = c.fetchone()
    s1 = row[1]
    s2 = row[2]

    # Get all run information
    with conn:
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
    row = c.fetchall()[0]

    lastid          = row[0]
    time_start      = row[1]
    max_requests    = row[4]
    scan_frequency  = row[5]
    interval        = row[6]
    factor0         = row[7]
    factor1         = row[8]
    factor2         = row[9]
    factor3         = row[10]
    factor4         = row[11]
    factor5         = row[12]
    factor6         = row[13]
    name0           = row[14]
    name1           = row[15]
    name2           = row[16]
    name3           = row[17]
    name4           = row[18]
    name5           = row[19]


    # Pull down selection options
    if value    == 'AIN0':
        i       = 2
        ymax    = 6 * factor0
        name    = name0
        color   = 'red'

    elif value  == 'AIN1':
        i       = 3
        ymax    = 6 * factor1
        name    = name1
        color   = 'green'

    elif value  == 'AIN2':
        i       = 4
        ymax    = 6 * factor2
        name    = name2
        color   = 'yellow'

    elif value  == 'AIN3':
        i       = 5
        ymax   == 100
        name    = name3
        color   = 'blue'

    elif value  == 'AIN4':
        i       = 6
        ymax    = 6 * factor4
        name    = name4
        color   = 'purple'
        counts = 0  
        
    elif value  == 'AIN5':
        i       = 7
        ymax    = 1 * factor5
        name    = name5

    if i == None:

        return {'data':[],'layout':[]}
    
    else:    
        # Append or continue current recording 
        avgs = lj.labjack(scan_frequency, max_requests, s1, s2)

        avgs.update({
            'AIN0':(avgs.get('AIN0') * factor0),
            'AIN1':(avgs.get('AIN1') * factor1),
            'AIN2':(avgs.get('AIN2') * factor2),
            'AIN3':(10**(avgs['AIN3']-6.125)*10000000),
            'AIN4':(avgs.get('AIN4') )
            })

        #print(avgs)
        rec.record_avgs(lastid,avgs)  # Writes the data to disk

        if value != 'AIN4':
        
            with conn:
                c.execute("SELECT * FROM dac_readings WHERE run_id = '{}' ORDER BY time DESC LIMIT 300 ".format(lastid))
            row = c.fetchall()


            data_dict = {'x':[],'y':[]}

            for d in row:
                data_dict['x'].append((d[1]-time_start)/1000000) # Calculate run time
                data_dict['y'].append(d[i] )

            x_data = data_dict.get('x')
            y_data = data_dict.get('y')

        if value == 'AIN4':

            with conn:
                c.execute(
                    f""" 
                    SELECT 
                        time, 
                        ain4, 
                        avg(ain4) 
                    OVER
                        (ORDER BY time ROWS BETWEEN 10 PRECEDING AND 0 FOLLOWING )
                    AS ma
                    FROM 
                        dac_readings WHERE run_id = '{lastid}' 
                    ORDER BY time DESC 
                    LIMIT 300
                    """
                    )
                    #.format(lastid))

                # print(
                #     f""" 
                #     SELECT time, ain4, avg(ain4) 
                #     OVER
                #     (ORDER BY time BETWEEN time >='{(int(datetime.now().strftime('%s%f'))-1000000)}' AND time <= '{int(datetime.now().strftime('%s%f'))} ')
                #     AS ain4mov
                #     FROM dac_readings WHERE run_id = '{lastid}' ORDER BY time DESC LIMIT 300
                #     """)

                #   """ 
                    # SELECT
                    #     sec,
                    #     cps,
                    #     AVG(cps) OVER (ORDER BY sec ROWS BETWEEN 10 PRECEDING AND 0 FOLLOWING ) AS mavg
                    # FROM
                    #     (SELECT ( ROUND( time/1000000, 0)+ 1 ) * 1000000 AS sec,
                    #             SUM(ain4) AS cps
                    #         FROM
                    #             dac_readings
                    #         WHERE
                    #             run_id = '{}'
                    #         GROUP BY
                    #             sec
                    #     ) AS td
                    # ORDER BY sec DESC
                    # LIMIT 60

                        # """
            
            row = c.fetchall()


            data_dict = {'x':[],'y':[]}

            for d in row:
                data_dict['x'].append((d[0]-time_start)/1000000) # Calculate run time
                data_dict['y'].append(d[2] * scan_frequency / max_requests)

            x_data = data_dict.get('x')
            y_data = data_dict.get('y')

        #print(x_data,y_data)
        traces = []
        traces.append(
            go.Scattergl(
                x = x_data,
                y = y_data,
                name = name,
                marker = dict(color = color,size = 3),
                mode = 'lines+markers'
                )
        )

        #Layout object defines the style of the graph features, eg axies titles etc
        layout = go.Layout(
            margin=go.layout.Margin(
                l=50,r=30, b=30, t=30),
                title = "",
                height = 800,
            showlegend=False,
            xaxis = dict(
                title = 'time', 
                visible = True),
            yaxis=dict(
                title = name,   
                visible = True, 
                autorange = True,
                #range = [0,ymax]
                )

            )  

        #The fig object is returned to place the placeholder graph.

        fig = {'data':traces,'layout':layout}

        

    return fig
