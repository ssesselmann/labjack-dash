import dash
#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from server import app
import dash_daq as daq
import tkinter as tk
import time
import sqlite3 as sql
from datetime import datetime

def tab4():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM preferences")
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
        xpoints         = prefs[19]

    tab4 = html.Div([ #main page

            html.Div(  # Heading
                'LabJack U3 Setup  & Calibration Last Run: ',
                style={
                    'width':'100%', 
                    'height':40, 
                    'marginTop':0,
                    'textAlign':'center',
                    'fontSize':30,
                    'color':'black', 
                    'backgroundColor':'lightgray',}
                    ),

            html.Div([html.P(['My project title: ',
                
                dcc.Input(
                    id="my_heading", 
                    type="text",
                    value= heading, 
                    placeholder="my title",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black',}
                        )]),

            html.Div([html.P(['Scan Frequency (max 50,000 Hz : n channels): ',
                dcc.Input(
                    id='scan_frequency', 
                    type="number",
                    value= scan_frequency,
                    debounce=True, 
                    placeholder="scan_frequency",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black',}
                        )]),

            html.Div([html.P(['Screen refresh interval millisec (min 200): ',
                dcc.Input(
                    id="interval", 
                    type="number",
                    value = interval,
                    debounce=True, 
                    placeholder="refresh_interval",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black', }
                        )]),

            html.Div([html.P(['Number of data points on charts (x axis): ',
                dcc.Input(
                    id="xpoints", 
                    type="number",
                    value = xpoints,
                    debounce=True, 
                    placeholder="xpoints",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black', }
                        )]),
            
            html.Div(['Channel Calibration Factors'],
            style={
                'width':'100%', 
                'height':40, 
                'padding': 5,
                'marginTop':0,
                'textAlign':'center',
                'fontSize':30,
                'color':'black', 
                'backgroundColor':'lightgray', 
                }),    

            html.Div([html.P(['Factor 0: ',
                dcc.Input(
                    id="factor0", 
                    type="number",
                    value= factor0,
                    debounce=True, 
                    placeholder="channel0",),],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Name 0: ',
                dcc.Input(
                    id='name0', 
                    type="text",
                    placeholder="AIN0",
                    value = name0,
                    )],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Factor 1: ',
                dcc.Input(
                    id="factor1", 
                    type="number",
                    value= factor1,
                    debounce=True, 
                    placeholder="channel1",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Name 1: ',
                dcc.Input(
                    id="name1", 
                    type="text",
                    placeholder="AIN1",
                    value = name1,)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Factor 2: ',
                dcc.Input(
                    id="factor2", 
                    type="number",
                    value= factor2,
                    debounce=True, 
                    placeholder="channel2",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Name 2: ',
                dcc.Input(
                    id="name2", 
                    type="text",
                    value= name2,
                    debounce=True, 
                    placeholder="AIN2",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Factor 3: ',
                dcc.Input(
                    id="factor3", 
                    type="number",
                    value= factor3,
                    debounce=True, 
                    placeholder="channel3",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Name 3: ',
                dcc.Input(
                    id="name3", 
                    type="text",
                    value= name3,
                    debounce=True, 
                    placeholder="AIN3",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),


            html.Div([html.P(['Factor 4: ',
                dcc.Input(
                    id="factor4", 
                    type="number",
                    value= factor4,
                    debounce=True, 
                    placeholder="channel4",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Name 4: ',
                dcc.Input(
                    id="name4", 
                    type="text",
                    value= name4,
                    debounce=True, 
                    placeholder="AIN4",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Slider 1 factor: ',
                dcc.Input(
                    id="factor5", 
                    type="number",
                    value= factor5,
                    debounce=True, 
                    placeholder="channel4",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Slider 1 name: ',
                dcc.Input(
                    id="name5", 
                    type="text",
                    value= name5,
                    debounce=True, 
                    placeholder="DAC0",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Slider 2 factor: ',
                dcc.Input(
                    id="factor6", 
                    type="number",
                    value= factor6,
                    debounce=True, 
                    placeholder= 'DAC1',)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(['Slider 2 name: ',
                dcc.Input(
                    id="name6", 
                    type="text",
                    value= name6,
                    debounce=True, 
                    placeholder="DAC0",)],
                    style={
                        'width':'100%', 
                        'marginTop': 0,
                        'padding': 5,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black'}
                        )]),

            html.Div([html.P(id='max_requests_output')],style={'visibility': 'hidden'}), 
            html.Div([html.P(id='max_requests_output2')],style={'visibility': 'hidden'}), 
            html.Div([html.P(id='my_heading_output')],style={'visibility': 'hidden'}),  
            html.Div([html.P(id='scan_frequency_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='interval_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='factor0_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='factor1_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='factor2_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='factor3_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='factor4_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='factor5_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='factor6_output')],style={'visibility': 'hidden'}),

            html.Div([html.P(id='name0_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='name1_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='name2_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='name3_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='name4_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='name5_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='name6_output')],style={'visibility': 'hidden'}),
            html.Div([html.P(id='xpoints_output')],style={'visibility': 'hidden'}),
            ])
         
    return tab4

#---------Callbacks-------------------------------------------------------------------------------------

@app.callback( # HEADING
    Output(component_id='my_heading_output', component_property='children'),
    Input(component_id='my_heading', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET heading = '{}' WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value)

#----------------------------------------------------------------------------------------------------------

@app.callback( # SCAN_FREQUENCY
    Output(component_id='scan_frequency_output', component_property='children'),
    Output(component_id='max_requests_output', component_property='children'),
    Input(component_id='scan_frequency', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET scan_frequency = {} WHERE id = 1 " .format(str(value)))   

    with conn: 
        c.execute("SELECT * FROM preferences ")
        prefs = c.fetchone()
        scan_frequency  = prefs[3]
        interval        = prefs[4]
        max_requests = scan_frequency/(1000/interval)

    with conn:
        c.execute("UPDATE preferences SET max_requests = {} WHERE id = 1 ".format(max_requests))

    return ['Output: {}'.format(value), 'Number of data requests averaged: {}'.format(max_requests)]

#----------------------------------------------------------------------------------------------------------

@app.callback( # INTERVAL
    Output(component_id='interval_output', component_property='children'),
    Output(component_id='max_requests_output2', component_property='children'),
    Input(component_id='interval', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
   
    with conn:
        c.execute("UPDATE preferences SET interval = {} WHERE id = 1 " .format(str(value))) 
    
    with conn: 
        c.execute("SELECT * FROM preferences ")
        prefs = c.fetchone()
        scan_frequency  = prefs[3]
        interval        = prefs[4]
        max_requests = scan_frequency/(1000/interval)

    with conn:
        c.execute("UPDATE preferences SET max_requests = {} WHERE id = 1 ".format(max_requests))

    return ['Output: {}'.format(value), 'Number of data requests averaged: {}'.format(max_requests)]
#----------------------------------------------------------------------------------------------------------

@app.callback( # FACTOR0
    Output(component_id='factor0_output', component_property='children'),
    Input(component_id='factor0', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET factor0 = {} WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value)
#----------------------------------------------------------------------------------------------------------

@app.callback( # FACTOR1
    Output(component_id='factor1_output', component_property='children'),
    Input(component_id='factor1', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET factor1 = {} WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value)

#----------------------------------------------------------------------------------------------------------

@app.callback( # FACTOR2
    Output(component_id='factor2_output', component_property='children'),
    Input(component_id='factor2', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET factor2 = {} WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value)

#----------------------------------------------------------------------------------------------------------

@app.callback( # FACTOR3
    Output(component_id='factor3_output', component_property='children'),
    Input(component_id='factor3', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET factor3 = {} WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value)            

#----------------------------------------------------------------------------------------------------------

@app.callback( # FACTOR4
    Output(component_id='factor4_output', component_property='children'),
    Input(component_id='factor4', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET factor4 = {} WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value) 

#----------------------------------------------------------------------------------------------------------

@app.callback( # FACTOR5
    Output(component_id='factor5_output', component_property='children'),
    Input(component_id='factor5', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET factor5 = {} WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value) 

#----------------------------------------------------------------------------------------------------------

@app.callback( # FACTOR6
    Output(component_id='factor6_output', component_property='children'),
    Input(component_id='factor6', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET factor6 = {} WHERE id = 1 " .format(str(value)))   
    return 'Output: {}'.format(value) 

#----------------------------------------------------------------------------------------------------------

@app.callback( # NAME0
    Output(component_id='name0_output', component_property='children'),
    Input(component_id='name0', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET name0 = '{}' WHERE id = 1 " .format(value))  
     
    return 'Output: {}'.format(value)     

#----------------------------------------------------------------------------------------------------------

@app.callback( # NAME1
    Output(component_id='name1_output', component_property='children'),
    Input(component_id='name1', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET name1 = '{}' WHERE id = 1 " .format(value))  
  
    return 'Output: {}'.format(value)     

#----------------------------------------------------------------------------------------------------------

@app.callback( # NAME2
    Output(component_id='name2_output', component_property='children'),
    Input(component_id='name2', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET name2 = '{}' WHERE id = 1 " .format(value))  
     
    return 'Output: {}'.format(value)  

#----------------------------------------------------------------------------------------------------------

@app.callback( # NAME3
    Output(component_id='name3_output', component_property='children'),
    Input(component_id='name3', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET name3 = '{}' WHERE id = 1 " .format(value))  
    
    return 'Output: {}'.format(value)          

#----------------------------------------------------------------------------------------------------------

@app.callback( # NAME4
    Output(component_id='name4_output', component_property='children'),
    Input(component_id='name4', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET name4 = '{}' WHERE id = 1 " .format(value))  
   
    return 'Output: {}'.format(value)                    

#----------------------------------------------------------------------------------------------------------

@app.callback( # NAME5
    Output(component_id='name5_output', component_property='children'),
    Input(component_id='name5', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET name5 = '{}' WHERE id = 1 " .format(value))  
   
    return 'Output: {}'.format(value) 

#----------------------------------------------------------------------------------------------------------

@app.callback( # NAME6
    Output(component_id='name6_output', component_property='children'),
    Input(component_id='name6', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET name6 = '{}' WHERE id = 1 " .format(value))  
   
    return 'Output: {}'.format(value)      

#----------------------------------------------------------------------------------------------------------

@app.callback( # XPOINTS
    Output(component_id='xpoints_output', component_property='children'),
    Input(component_id='xpoints', component_property='value'))

def heading(value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    with conn:
        c.execute("UPDATE preferences SET xpoints = '{}' WHERE id = 1 " .format(value))  
   
    return 'Output: {}'.format(value)      









