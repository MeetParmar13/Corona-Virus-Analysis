import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output


external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': "stylesheet",
        'Integrity': 'shals4-08/SFPGESFIT300ngsV7Z2701uXPkF0wHERkLPO',
        'crossorigin': 'anonymous'
    }
]

# Load Data
pat = pd.read_csv('IndividualDetails.csv')
total = pat.shape[0]
active = pat[pat['current_status'] == 'Hospitalized'].shape[0]
recovered = pat[pat['current_status'] == 'Recovered'].shape[0]
deaths = pat[pat['current_status'] == 'Deceased'].shape[0]

# Dropdown Options for Status
option = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'},
]

# Data Cleaning and Age Group Calculation
pat = pat.dropna(subset=['age'])
pat['age'] = pd.to_numeric(pat['age'], errors='coerce')
pat['age'] = pat['age'].fillna(5)
pat['age'] = pat['age'].astype(int)

# Create Age Groups
bins = [0, 20, 40, 60, 80, 100]
labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
pat['age_group'] = pd.cut(pat['age'], bins=bins, labels=labels, right=False)

# Calculate Counts for Age Groups
age_gb = pat['age_group'].value_counts().reset_index()
age_gb.columns = ['age_group', 'count']

# Create Pie Chart
fig = px.pie(
    age_gb,
    names='age_group',
    values='count',
    title="Age Distribution in Pie Chart"
)

# Create Dash App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# App Layout
app.layout = html.Div([
    html.H1("Corona Virus Pandemic ", style={'text-align': 'center', 'color': '#ffff'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Total Case', className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Active', className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Recovered', className='text-light'),
                    html.H4(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Death', className='text-light'),
                    html.H4(deaths, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3'),
    ], className='row'),

    # Pie Chart Graph Section
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='pie', figure=fig)  # Add the pie chart here
                ], className='card-body')
            ], className='card')
        ], className='col-md-6'),
        html.Div([
            
        ], className='col-md-6')
    ], className='row'),

    # Dropdown and Bar Graph Section
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='meet', options=option, value='All'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row')

], className='container')

# Callback to update the Bar Chart
@app.callback(
    Output('bar', 'figure'),
    [Input('meet', 'value')]
)
def update_bar_chart(type):
    if type == 'All':
        pbar = pat['detected_state'].value_counts().reset_index()
        return {
            'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout': go.Layout(title='State Total Count')
        }
    else:
        npat = pat[pat['current_status'] == type]
        pbar = npat['detected_state'].value_counts().reset_index()
        return {
            'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout': go.Layout(title='State Total Count')
        }


@app.callback(
    Output('pie', 'figure'),
    [Input('meet', 'value')]
)
def update_pie_chart(type):
    if type == 'All':
        age_gb = pat['age_group'].value_counts().reset_index()
    else:
        npat = pat[pat['current_status'] == type]
        age_gb = npat['age_group'].value_counts().reset_index()
    
    age_gb.columns = ['age_group', 'count']
    fig = px.pie(
        age_gb,
        names='age_group',
        values='count',
        title="Age Distribution in Pie Chart"
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
