# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash import Input, Output

external_stylesheets = [dbc.themes.PULSE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create a dataframe from existing CSV file with the prepared dataset
df = pd.read_csv('prepared_dataset.csv')

journey_types = df.iloc[:, 5:]

types = journey_types.columns

line_fig = px.line(df, x="Period ending", y=df.columns[5:], markers=True,
                   title="Usage of public transport by journey types in London", width=1200, height=500,
                   labels={"Period ending": "Period ending (date)", "value": "Amount of journeys (millions)",
                           "variable": "Journey types:"})

app.layout = html.Div(children=[

    html.Div(children=[dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Page 1", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="NavbarSimple",
        brand_href="#",
        color="primary",
        dark=True,
    )]),

    html.H1(
        children='Exploratory analysis on how public transport use in London has changed due to the coronavirus pandemic'),

    html.Div(children='''
        There are many types of public transportation in London. Trends in the usage of public transport change due to
        the certain events such as road closures, construction works and so on. In 2020 and 2021, there were a lot of
        disruptions of Transport for London (TfL) because of coronavirus pandemic. New regulations and changes led to
        the transition of popularity for public transport journeys by type of transport. Due to an increased demand for
        transport, there is now a problem of overcrowding, which is a safety risk.
    '''),

    html.Div(
        [dcc.Dropdown(
            id="journey-types-dropdown",
            options=[{
                'label': i,
                'value': i
            } for i in types],
            value=types),
        ],
        style={'width': '30%',
               'display': 'inline-block'}),

    dcc.Graph(
        id='line-graph',
        figure=line_fig
    ),

    html.Button(children="Button", className="btn btn-primary")
])

@app.callback(
    Output(component_id='line-graph', component_property='figure'),
    Input(component_id='journey-types-dropdown', component_property='value')
)
def update_graph(selected_type):
    filtered_journeys = df[['Period ending', f'{selected_type}']]
    line_fig = px.line(filtered_journeys, x='Period ending', y=f'{selected_type}',
                       title=f'Usage of {selected_type} in London')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
