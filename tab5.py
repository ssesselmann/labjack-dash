
import dash
import dash_daq as daq
#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
import tkinter as tk
import sqlite3 as sql
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from server import app
import base64


def tab5():

    app = dash.Dash()
    image_filename = 'assets/banner.png'
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    tab5 = html.Div([

        html.H1(children='Labjack U3 Project',style={'textAlign':'center', 'padding':'10px'}),
        
        html.P(children="""
            Ater a long struggle with a big brand name DAC on Windows, 
            and decided to go with Linux and write my own code (as one does).""",
            style={'textAlign':'left', 'marginLeft':'100px', 'marginRight': '100px'}),

        html.P(children="""    
            I wrote this program for the LabJack U3, it controls the two analogue outputs and records 5 inputs. 
            The calibration tab allows you to name your project and calibrate each instrument separately. 
            The program is free for anyone to use, and I hope the many hours I spent coding will somehow contribute to your scientific research.
            """, 
            style={'textAlign':'left', 'marginLeft':'100px', 'marginRight': '100px'}),
        html.P(children="""
            If you have any suggestions for improvements or any questions about the program, feel free to email me suggestions. 
            """, 
            style={'textAlign':'left', 'marginLeft':'100px', 'marginRight': '100px'}),
        html.H2(children="Acknowledgements", 
            style={'textAlign':'center', 'marginLeft':'100px', 'marginRight': '100px'}),
        html.P(children="""
            First of all a big thanks to LabJack for making a low cost high quality DAC and
            thanks to my two sons Erik and Tom for patiently coaching me with the Python code.
            """, 
            style={'textAlign':'left', 'marginLeft':'100px', 'marginRight': '100px'}),
        html.P(children="Steven Sesselmann", 
            style={'textAlign':'left', 'marginLeft':'100px', 'marginRight': '100px'}),
        html.P(children="steven@gammaspectacular.com", 
            style={'textAlign':'left', 'marginLeft':'100px', 'marginRight': '100px'}),




        html.Div([dcc.Link('gammaspectacular.com', href='https://gammaspectacular.com',)], style={'textAlign':'center'}),


        # html.Img(src='data:image/png;base64,{}'.format(encoded_image)) ], style={'textAlign':'center'}),

        

        ]),


    return tab5