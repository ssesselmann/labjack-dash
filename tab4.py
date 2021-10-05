import dash
#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from server import app
import sqlite3 as sql
from datetime import datetime
import sqlite3 as sql

#---------------- Page Layout ------------------------------------------------------
def tab4():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn:
        c.execute("SELECT * FROM run_number ORDER BY run_id DESC LIMIT 1")

        lastrun = (c.fetchone()[0])-1


    tab4 = html.Div([

        html.P('Enter filename'),
        html.Div(dcc.Input(id='input_filename',value='data.csv',type='text')),
        html.Div(id='filename_output'),

        html.P('Enter run to export, last run was: {} '.format(lastrun)),
        html.Div(dcc.Input(id='input_run',value= 0 ,type='number',debounce=True)),
        html.Div('Run: ',id='data_output'),

        html.Button('Save', id='button',value='n_clicks'),
        html.Div(id='button_output',style={'display':'none'}),       
        ],style={'padding':'50px', 'textAlign':'center'}),

    return tab4

#----------------------------------------------------------------------------------

@app.callback(
    Output('data_output','children'),
    Output('filename_output', 'children'),
    Output('button_output', 'children'),
    [Input('button', 'n_clicks')],
    [State('input_run','value')],
    [State('input_filename', 'value')]
    )

def exportcsv(n,value,path):

    print(str(path))

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    if value > 0:
        with conn:
            c.execute("SELECT * FROM run_number WHERE run_id = {} ".format(str(value)))

            run = c.fetchall()[0]
            runid   = run[0]

        with conn:
            c.execute("SELECT * FROM preferences")   
            prefs   = c.fetchone()

            name0   = prefs[12]
            name1   = prefs[13]
            name2   = prefs[14]
            name3   = prefs[15]
            name4   = prefs[16]
            name5   = prefs[17]
            name6   = prefs[18]
            run     =  'run'
            time    = 'time'


        with conn:
            c.execute("SELECT * FROM dac_readings WHERE run_id = {} ORDER BY time ".format(str(value)))

        readings = c.fetchall()

        with open(str(path), 'w') as fd:

            header = ','.join(str(j) for j in [(run),(time),(name0),(name1),(name2),(name3),(name4)]) +'\n'
                
            fd.write(header)

        for i in range(len(readings)):

            string = ','.join(str(j) for j in [(readings[i][0]),(readings[i][1]),(readings[i][2]),(readings[i][3]),(readings[i][4]),(readings[i][5]),(readings[i][6])]) +'\n'

            with open(str(path),'a') as fd:
                fd.write(string)
        
    return [value,path,n]


