import json
from server import app
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import sqlite3 as sql

run = None

def tab3():

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()

    with conn:
        c.execute('SELECT run_id FROM run_number ORDER BY run_id DESC LIMIT 20')
        run = c.fetchall()
        options = []
        
        for i in range(20):       
            runs = {'label':run[i][0], 'value':run[i][0]}
            options.append(runs)    
            
    tab3 = html.Div([
            html.Div([html.P([
                
                dcc.Dropdown(
                    id="run", 
                    options= options,
                    placeholder="select run",)],
                    style={
                        'width':'100px', 
                        'marginTop': 0,
                        'padding': 10,
                        'height':20, 
                        'textAlign':'center',
                        'fontSize':16,
                        'color':'black',}
                        )],
                    style={'width': '100%', 'height': '50px', 'backgroundColor':'gray'},),

            html.Div(dcc.Graph( id='analysis' ),
                    style = {'width':'98%', 'textAlign':'center', 'border':'3px gray solid','display':'inline-block'},
        ),

            html.Div([
                      dcc.Input(id='input', type='text'),
                        html.Button('Delete This Run', id='button', n_clicks=0, style={'backgroundColor':'red', 'fontWeight':'bold', 'color':'white'}),
                        html.Div(children='Can not be undone !'),
                       html.Div(id='delete_output')
                 ])
            ])

    return tab3

@app.callback(
    Output('analysis', 'figure'),
    Input('run', 'value'),
    )

def analysis(value):

    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    
    data = []
    time = []
    ain0 = []
    ain1 = []
    ain2 = []
    ain3 = []
    ain4 = []
    
    with conn:
        c.execute(f"SELECT time_start FROM run_number WHERE run_id = {str(value)}")    
        time_start = c.fetchone()[0] 

    with conn:
        c.execute(f"SELECT run_id, (time - {time_start} ) AS time, ain0, ain1, ain2, ain3 FROM dac_readings WHERE run_id = {str(value)} ORDER BY TIME DESC")
        data = c.fetchall()

        for i in range(len(data)):
            runid = data[i][0]
            time.append(data[i][1]/1000000)
            ain0.append(data[i][2])
            ain1.append(data[i][3])
            ain2.append(data[i][4])
            ain3.append(data[i][5])
            
    with conn:
        c.execute(f"""
            SELECT (time - {time_start}) AS time, ((ain4 - LAG (ain4, 100) OVER (ORDER BY time)) / (time - LAG (time, 100) OVER (ORDER BY time)))*1000000 AS cps 
            FROM dac_readings WHERE run_id = {str(value)} ORDER BY TIME DESC;""")

        counts = c.fetchall()
        
        for i in range(len(data)):
            ain4.append(counts[i][1])

    with conn:
        c.execute("SELECT * FROM preferences")
        prefs = c.fetchone()

        name0     = prefs[12]
        name1     = prefs[13]
        name2     = prefs[14]
        name3     = prefs[15]
        name4     = prefs[16]

        max0      = prefs[20]
        max1      = prefs[21]
        max2      = prefs[22]
        max3      = prefs[23]
        max4      = prefs[24]
        max5      = prefs[25]
        max6      = prefs[26]
     

    traces = []
    traces.append(
        go.Scattergl(
            x = time,
            y = ain0,
            name = name0,
            yaxis='y',
            marker = dict(color = 'red', size = 3),
            mode = 'lines+markers'
            )
        )

    traces.append(
        go.Scattergl(
            x = time,
            y = ain1,
            name = name1,
            yaxis='y2',
            marker = dict(color = 'green', size = 3),
            mode = 'lines+markers'
            )
        )

    traces.append(
        go.Scattergl(
            x = time,
            y = ain2,
            name = name2,
            yaxis='y2',
            marker = dict(color = 'orange', size = 3),
            mode = 'lines+markers'
            )
        )

    traces.append(
        go.Scattergl(
            x = time,
            y = ain3,
            name = name3,
            yaxis='y4',
            marker = dict(color = 'blue', size = 3),
            mode = 'lines+markers'
            )
        )

    traces.append(
        go.Scattergl(
            x = time,
            y = ain4,
            name = name4,
            yaxis='y5',
            marker = dict(color = 'purple', size = 3),
            mode = 'lines+markers'
            )
        )


    #Layout object defines the style of the graph features, eg axies titles etc
    layout = go.Layout(
            margin=go.layout.Margin(l=100,r=100, b=30, t=30),
            title="",
            height = 800,
            autosize=True,
            showlegend=True,
            xaxis = dict(title = 'Seconds', visible = True),

            yaxis = dict(
                title       = name0, 
                type        = 'linear', 
                visible     = True, 
                autorange   = True,
                #range      = [0, max0], 
                color       = 'red', 
                anchor      = 'free', 
                # overlaying  = 'y', 
                side        = 'left', 
                position    = 0.00, 
                automargin  = True),
            
            yaxis2= dict(
                title       = name1, 
                type        = 'linear',
                visible     = True, 
                #range      = [0, max1], 
                autorange   = True,
                color       = 'green', 
                anchor      = 'free', 
                # overlaying  = 'y', 
                side        = 'left', 
                position    = 0.01, 
                automargin  = True),

            yaxis3= dict(
                title       = name2, 
                type        = 'linear',
                visible     = True, 
                #range      = [0, max2],
                autorange   = True, 
                color       = 'orange', 
                anchor      = 'free', 
                # overlaying  = 'y', 
                side        = 'left', 
                position    = 0.02, 
                automargin  = True),
            
            yaxis4= dict(
                title       = name3,
                type        = 'linear',
                visible     = True, 
                #range      = [0, max3],
                autorange   = True, 
                color       = 'blue', 
                anchor      = 'free', 
                # overlaying  = 'y', 
                side        = 'right', 
                position    = 1.00, 
                automargin  = True),

            yaxis5= dict(
                title       = name4, 
                type        = 'linear',
                visible     = True, 
                #range      = [0, max4],
                autorange   = True, 
                color       = 'purple', 
                anchor      = 'free', 
                # overlaying  = 'y', 
                side        = 'right', 
                position    = 0.99, 
                automargin  = True)
        )  

    #The fig object is returned to place the placeholder graph.
    fig = {'data':traces,'layout':layout}    


    return fig

@app.callback(
    Output('delete_output', 'children'),
    [Input('button', 'n_clicks')], 
    [State('input', 'value')]
    )

def delete(n, value):
    conn = sql.connect("labjackdb.db")
    c = conn.cursor()
    if value != None:
        with conn:
            c.execute(f"DELETE FROM dac_readings WHERE run_id = {value}")
            c.execute(f"DELETE FROM run_number WHERE run_id = {value}")
        return f'Deleted run {value} from database!!'
