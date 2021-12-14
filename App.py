import dash
import lj as lj
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from server import app
from tab1 import tab1
from tab2 import tab2
from tab3 import tab3
from tab4 import tab4
from tab5 import tab5
from tab6 import tab6
from tab7 import tab7


#---Defines the tab buttons------------------------------------------------------------

app.layout = html.Div([
    dcc.Tabs(
        id="tabs", 
        value='tab1', 
        style={'fontWeight': 'bold'}, 
        children=[
        dcc.Tab(
            label='Controls', 
            value='tab1'),
        dcc.Tab(
            label='Charts', 
            value='tab2'), 
        dcc.Tab(
            label='Post analysis', 
            value='tab3'),       
        dcc.Tab(
            label='Data Download', 
            value='tab4'),              
        dcc.Tab(
            label='Calibration', 
            value='tab5'),
        dcc.Tab(
            label='Info', 
            value='tab6'),   
        dcc.Tab(
            label='Exit', 
            value='tab7'),        
        ]),

    html.Div(id = 'tabs-content'),
    dcc.Interval(
            id='write_readings',
            interval= 1000, 
            n_intervals=0,
            disabled=False 
            ),
    html.Div(id='wr')
    ])

#---Tab values call function and provide page contents

@app.callback(
    Output('tabs-content','children'),
    Input('tabs','value'))

def render_content(tab):

    if tab == 'tab1':
        return tab1()
        
    elif tab == 'tab2':
        return tab2()

    elif tab == 'tab3':
        return tab3()    

    elif tab == 'tab4':
        return tab4() 

    elif tab == 'tab5':
        return tab5()   

    elif tab == 'tab6':
        return tab6()  
    
    elif tab == 'tab7':
        return tab7() 
            

@app.callback(
    Output('wr','children'),
    Input('write_readings','n_intervals'))

def start_labjack(n):
    if n == 0:
        lj.labjack()
    


