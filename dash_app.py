# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html

external_stylesheets = [dbc.themes.PULSE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create a dataframe from existing CSV file with the prepared dataset
df = pd.read_csv('prepared_dataset.csv')

fig = px.line(df, x="Period ending", y="Bus journeys (m)", markers=True,
              title="Usage of public transport by journey types in London")

app.layout = html.Div(children=[
    html.H1(children='Coursework 1'),

    html.Div(children='''
        Dataframe with the amount of journeys for different types of public transportation in London:
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.Button(children="Button", className="btn btn-primary")
])

if __name__ == '__main__':
    app.run_server(debug=True)
