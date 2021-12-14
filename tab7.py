
import dash
import dash_daq as daq
import sys
from dash import dcc
from dash import html
import multiprocessing
import time
from dash.dependencies import Input, Output
from server import app
from flask import request

def tab7():

    tab7 = html.Div([ 
        html.H1(
        children='Thanks for using LabDash, see you back soon!',
        style={'textAlign':'center', 'padding':'10px'}
        ),
        html.Button(
            id='exit', 
            children='Click to confirm exit',
            style={'textAlign':'center', 'padding':'10px', 'backgroundColor':'red', 'fontWeight':'bold', 'width':300}),
        html.P(
        children='Always exit the program by clicking the red button, this prevents processes running after browser window is closed.',
        style={'textAlign':'center', 'padding':'10px'}
        ),
        ],style={'textAlign':'center'}),
    return tab7

@app.callback(Output(component_id='exit', component_property='children'), 
    Input(component_id='exit', component_property='n_clicks'
        ))
def prog_exit(n):

    if (n != None): 
        shutdown()
        return 'Program closed'
    else:
        return 'Click to confirm exit'

def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    