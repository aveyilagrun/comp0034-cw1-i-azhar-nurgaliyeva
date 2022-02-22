import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output
from datetime import datetime

external_stylesheets = [dbc.themes.PULSE]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create a dataframe from existing CSV file with the prepared dataset
df = pd.read_csv('prepared_dataset.csv')

journey_types = df.iloc[:, 5:]
types = journey_types.columns

df['Period ending'] = pd.to_datetime(df['Period ending'])


line_fig = px.line(df, x="Period ending", y=df.columns[5:], markers=True,
                   title="Usage of public transport by journey types in London", width=1200, height=500,
                   labels={"Period ending": "Period ending (date)", "value": "Amount of journeys (millions)",
                           "variable": "Journey types:"})

bar_fig = px.bar(df, x="Period ending", y=df.columns[5:],
                 title="Cumulative usage of public transport by journey types in London", width=1200, height=500,
                 labels={"index": "Period ending (date)", "value": "Amount of journeys (millions)",
                         "variable": "Journey types:"})

pie_df = df[
    ['Bus journeys (m)', 'Underground journeys (m)', 'DLR journeys (m)', 'Tram journeys (m)', 'Overground journeys (m)',
     'Emirates Airline journeys (m)', 'TfL Rail journeys (m)']].sum()

pie_fig = px.pie(values=pie_df.values, names=pie_df.index, title="Amount of journeys in a year")

# Graph to compare same periods from different financial years?

app.layout = html.Div(children=[

    html.Div(children=[dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(
                "Exploratory analysis on how public transport use in London has changed due to the coronavirus pandemic",
                href="#"))
        ],
        brand="COMP0034: Coursework 1",
        brand_href="#",
        color="primary",
        dark=True,
    )]),

    html.Div([html.H4('Description of the data'),
              html.Div('''There are many types of public transportation in London. Trends in the usage of 
                       public transport change due to the certain events such as road closures, construction works 
                       and so on. In 2020 and 2021, there were a lot of disruptions of Transport for London (TfL) 
                       because of coronavirus pandemic. New regulations and changes led to the transition of popularity 
                       for public transport journeys by type of transport. Due to an increased demand for transport, 
                       there is now a problem of overcrowding, which is a safety risk.''')]),

    html.Div(html.H4('Choose a journey type from the dropdown list:')),

    html.Div(
        dcc.Dropdown(
             id="journey-types-dropdown",
             options=[{
                 'label': i,
                 'value': i
             } for i in types], placeholder='Select a journey type...'),
        style={'width': '40%',
               'display': 'inline-block'}),

    html.Div(dcc.Graph(
        id='line-graph',
        figure=line_fig
    )),

    html.Div(dcc.Graph(
        id='bar-graph',
        figure=bar_fig
    )),

    html.Div(dcc.Graph(
        id='pie-graph',
        figure=pie_fig
    )),

    html.Div(dcc.RangeSlider(
        2018,
        2021,
        step=1,
        id='timeline-slider',
        value=[2019, 2020],
        marks={
            2018: '2018',
            2019: '2019',
            2020: '2020',
            2021: '2021'}
    ), style={'width': '50%', 'display': 'middle'})

])


# Callback for line graph
@app.callback(
    Output(component_id='line-graph', component_property='figure'),
    Input(component_id='journey-types-dropdown', component_property='value'))
def update_line_graph(selected_type):
    filtered_journeys = df[['Period ending', f'{selected_type}']]
    line_fig = px.line(filtered_journeys, x='Period ending', y=f'{selected_type}',
                       title=f'Usage of {selected_type} in London')
    return line_fig


# Callback for pie graph
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='timeline-slider', component_property='value'))
def update_pie_graph(selected_type):
    filtered_timeline = ...
    pie_fig = ...
    return pie_fig


if __name__ == '__main__':
    app.run_server(debug=True)
