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

journey_types = df.iloc[:, 5:]

types = journey_types.columns

fig = px.line(df, x="Period ending", y=df.columns[5:], markers=True,
              title="Usage of public transport by journey types in London", width=1200, height=500,
              labels={"Period ending": "Period ending (date)", "value": "Amount of journeys (millions)",
                      "variable": "Journey types:"})

app.layout = html.Div(children=[
    html.H1(
        children='Exploratory analysis on how public transport use in London has changed due to the coronavirus pandemic'),

    html.Div(children='''
        There are many types of public transportation in London. Trends in the usage of public transport change due to 
        the certain events such as road closures, construction works and so on. In 2020 and 2021, there were a lot of 
        disruptions of Transport for London (TfL) because of coronavirus pandemic. New regulations and changes led to 
        the transition of popularity for public transport journeys by type of transport. Due to an increased demand for 
        transport, there is now a problem of overcrowding, which is a safety risk.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.Button(children="Button", className="btn btn-primary")
])

if __name__ == '__main__':
    app.run_server(debug=True)
