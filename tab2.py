import dash
from dash import dcc
from dash import html
import time
from datetime import datetime
from dash.dependencies import Input, Output, State
from server import app
import sqlite3 as sql
import plotly.graph_objs as go
import sqlite3 as sql
import utilities as ut



#---------------- Page Layout ------------------------------------------------------

def tab2():

    time_start = int(datetime.now().strftime('%s%f'))

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn:
        c.execute("SELECT * FROM preferences")

        prefs = c.fetchone()

        interval = prefs[4]
        name0    = prefs[12]
        name1    = prefs[13]
        name2    = prefs[14]
        name3    = prefs[15]
        name4    = prefs[16]
        name5    = prefs[17]
        name6    = prefs[18]
        xpoints  = prefs[19]

    with conn:
        c.execute("SELECT * FROM sliderpos")
        spos = c.fetchone()
        chart = spos[3]    

    tab2 = html.Div([ dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': name0, 'value': 'AIN0'},
            {'label': name1, 'value': 'AIN1'},
            {'label': name2, 'value': 'AIN2'},
            {'label': name3, 'value': 'AIN3'},
            {'label': name4, 'value': 'AIN4'}
            ],style={'textAlign':'center'},
        
        value=chart, #default value

            ),

        html.Div(id='dd-output-container'),

        dcc.Interval(
        id='interval',
        interval=interval, 
        n_intervals=0),


        html.Div([ 
            dcc.Graph( id='graph' ),
            ],
            style = {'width':'100%',"border":"3px gray solid",'display':'inline-block'}
            )         
            ],
            style = {'color':'black'},

            )
    
    return tab2

#---------------- END PAGE LAYOUT ------------------------------------------------------    

@app.callback( 
    Output('graph','figure'),
    [Input('interval','n_intervals')],
    State('dropdown', 'value')
    )

def interval(n,value):

    i = None
    data_dict = {'x':[],'y':[]}

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    # Set last chart viewed
    with conn:
        c.execute(f"UPDATE sliderpos SET last_chart == '{value}' ")

    
    with conn:
        c.execute("SELECT * FROM preferences")
        prefs = c.fetchone()
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
        
        xpoints         = prefs[19]

        max0            = prefs[20]
        max1            = prefs[21]
        max2            = prefs[22]
        max3            = prefs[23]
        max4            = prefs[24]
        max5            = prefs[25]
        max6            = prefs[26]

    # Pull down selection options
    if value    == 'AIN0':
        i       = 1
        ymax    = 6 * factor0
        name    = name0
        color   = 'red'

    elif value  == 'AIN1':
        i       = 2
        ymax    = 6 * factor1
        name    = name1
        color   = 'green'

    elif value  == 'AIN2':
        i       = 3
        ymax    = 6 * factor2
        name    = name2
        color   = 'orange'

    elif value  == 'AIN3':
        i       = 4
        ymax    = 6 * factor3
        name    = name3
        color   = 'blue'

    elif value  == 'AIN4':
        i       = 5
        ymax    = 6 * factor4
        name    = name4
        color   = 'purple'
        

    if i == None:

        return {'data':[],'layout':[]}
    
    else:    

        state = ut.if_recording(c)

        table_name = "dac_readings" if state == True else "temp_readings"

        with conn:
            c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")
            run = c.fetchone()
            lastid = run[0]
            time_start = run[1]



        if (value <= 'AIN3'):
            c.execute(f"SELECT time, ain0, ain1, ain2, ain3 FROM {table_name} ORDER BY time DESC LIMIT 1200")
            readings = c.fetchall()

            for d in readings:
                data_dict['x'].append((d[0] - time_start)/1000000)
                data_dict['y'].append(d[i])

        if (value =='AIN4'):
            if state == False:
                lastid = 1
            c.execute(f"""
                    SELECT time, ((ain4 - LAG (ain4, 100) OVER (ORDER BY time)) / (time - LAG (time, 100) OVER (ORDER BY time)))*1000000 AS cps 
                    FROM {table_name} WHERE run_id = {lastid} ORDER BY TIME DESC LIMIT 1200;""")
            readings = c.fetchall()   

            for d in readings:    
                data_dict['x'].append((d[0]- time_start)/1000000)
                data_dict['y'].append(d[1])


        x_data = data_dict.get('x')
        y_data = data_dict.get('y')

        #print(x_data, y_data) #debug

        traces = []
        traces.append(
            go.Scattergl(
                x = x_data,
                y = y_data,
                name = name,
                marker = dict(color = color, size = 3),
                mode = 'lines+markers'
                )
            )

        #Layout object defines the style of the graph features, eg axies titles etc
        layout = go.Layout(
                margin=go.layout.Margin(
                l=50,r=30, b=30, t=30),
                title = "",
                height = 700,
                showlegend=False,

                xaxis = dict(title = 'time', visible = True),
                yaxis=dict(title = name, visible = True, autorange = True)#, range = [0,ymax])

            )  

        #The fig object is returned to place the placeholder graph.

        fig = {'data':traces,'layout':layout}

        

    return fig
