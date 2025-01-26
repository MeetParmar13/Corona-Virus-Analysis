import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import dash 
from dash import html,dcc
from dash.dependencies import Input,Output
  


external_stylesheets =[
   { 
   ' href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
    'rel': "stylesheet",
    'Integrity': 'shals4-08/SFPGESFIT300ngsV7Z2701uXPkF0wHERkLPO',
    'crossorigin':'anonymous'
}
]
pat=pd.read_csv('IndividualDetails.csv')
total=pat.shape[0]
active=pat[pat['current_status'] == 'Hospitalized'].shape[0]
recovered= pat[pat['current_status'] == 'Recovered'].shape[0]
deaths= pat[pat['current_status'] == 'Deceased'].shape[0]

print("Hello1")

option=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'},
]

print("Hello2")

app=dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout=html.Div([
    html.H1("Corona Virus Pandemic ",style={'text-align':'center','color':'#ffff'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Total Case',className='text-light'),
                    html.H4(total,className='text-light')
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-3'),
        html.Div([
             html.Div([
                html.Div([
                    html.H2('Active',className='text-light'),
                    html.H4(active,className='text-light')
                ],className='card-body')
            ],className='card bg-info')
        ],className='col-md-3'),
        html.Div([
             html.Div([
                html.Div([
                    html.H2('Recovered',className='text-light'),
                    html.H4(recovered,className='text-light')
                ],className='card-body')
            ],className='card bg-warning')
        ],className='col-md-3'),
        html.Div([
             html.Div([
                html.Div([
                    html.H2('Death',className='text-light'),
                    html.H4(deaths,className='text-light')
                ],className='card-body')
            ],className='card bg-success')
        ],className='col-md-3'),
    ],className='row'),


    html.Div([],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='meet',options=option,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')

],className='container')

@app.callback(Output('bar', 'figure'), [Input('meet', 'value')])
def updeated_graph(type):

    if type == 'All':
        pbar=pat['detected_state'].value_counts().reset_index()
        return  {
        'data':[go.Bar(x=pbar['detected_state'],y=pbar['count'])],
        'layout':go.Layout(title='State Total Count')
        }
    else:
        npta=pat[pat['current_status'] == type]
        pbar=npta['detected_state'].value_counts().reset_index()
if __name__ == "__main__":
    app.run_server(debug=True)
