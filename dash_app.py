""" Coursework 1 - Dash App """
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = [dbc.themes.PULSE]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

# Create a dataframe from existing CSV file with the prepared dataset
df = pd.read_csv('prepared_dataset.csv')

journey_types = df.iloc[:, 5:]
types = journey_types.columns
y_values = df.columns[5:]

df['Period ending'] = pd.to_datetime(df['Period ending'])

line_fig = px.line(df, x="Period ending", y=y_values, markers=True,
                   title="Usage of public transport by journey types in London",
                   width=1200, height=500,
                   labels={"Period ending": "Period ending (date)",
                           "value": "Amount of journeys (millions)",
                           "variable": "Journey types:"})

bar_fig = px.bar(df, x="Period ending", y=y_values,
                 title="Cumulative usage of public transport by journey types in London",
                 width=1200, height=500,
                 labels={"index": "Period ending (date)",
                         "value": "Amount of journeys (millions)",
                         "variable": "Journey types:"})

pie_df = df[['Bus journeys (m)', 'Underground journeys (m)', 'DLR journeys (m)',
             'Tram journeys (m)', 'Overground journeys (m)',
             'Emirates Airline journeys (m)', 'TfL Rail journeys (m)']].sum()

pie_fig = px.pie(values=pie_df.values, names=pie_df.index,
                 title="Amount of journeys in a year")

sub_fig = make_subplots(rows=2, cols=2,
                        subplot_titles=("Overground journeys", "DLR journeys",
                                        "Tram journeys", "TfL Rail journeys"))

sub_fig.add_trace(go.Scatter(x=df['Period ending'], y=df['Overground journeys (m)'] * 1000000),
                  row=1, col=1)

sub_fig.add_trace(go.Scatter(x=df['Period ending'], y=df['DLR journeys (m)'] * 1000000),
                  row=1, col=2)

sub_fig.add_trace(go.Scatter(x=df['Period ending'], y=df['Tram journeys (m)'] * 1000000),
                  row=2, col=1)

sub_fig.add_trace(go.Scatter(x=df['Period ending'], y=df['TfL Rail journeys (m)'] * 1000000),
                  row=2, col=2)

sub_fig.update_layout(height=500, width=1200,
                      title_text="Usage of overground, DLR, tram and "
                                 "TfL rail journey types in London")

box_fig = px.box(df, y=y_values)

line_graph_tab = html.Div([
    html.H5('Choose a journey type from the list:'),
    dcc.Dropdown(
        id="journey-types-dropdown",
        options=[{
            'label': i,
            'value': i
        } for i in types], placeholder='Select a journey type...'),

    dcc.Graph(
        id='line-graph',
        figure=line_fig
    ),
],
    style={'width': '40%', 'display': 'inline-block', 'margin-left': '30px',
           'margin-right': "30px", 'margin-top': "10px", 'textAlign': 'center'})

bar_graph_tab = html.Div([
    dcc.Graph(
        id='bar-graph',
        figure=bar_fig
    )
],
    style={'width': '40%', 'display': 'inline-block', 'margin-left': '30px', 'margin-right': "30px",
           'margin-top': "10px"})

pie_chart_tab = html.Div([
    dcc.Graph(
        id='pie-graph',
        figure=pie_fig
    ),

    html.H5('Choose a timeline to compare popularity in journey types:'),

    dcc.RangeSlider(min=18, max=21,
                    step=1,
                    id='timeline-slider',
                    value=[18, 21],
                    marks={
                        18: '2018',
                        19: '2019',
                        20: '2020',
                        21: '2021'}
                    ),
],
    style={'display': 'inline-block', 'margin-left': '80px',
           'margin-right': "20px", 'margin-top': "10px"})

subplots_tab = html.Div([
    html.H4('Subplots of Overground, Tram, DLR and TfL Rail journey types'),
    dcc.Graph(
        id='time-graph',
        figure=sub_fig
    )
], style={'margin-left': '30px', 'margin-right': "30px", 'margin-top': "10px"})

box_plots_tab = html.Div([
    html.H4('Box plots of amount of journeys'),
    html.H5('Choose journey types to compare box plots:'),

    dcc.RadioItems(
        id='y-axis',
        options=[{'value': x, 'label': x}
                 for x in y_values],
        value='Bus journeys (m)',
        labelStyle={'display': 'inline-block', 'margin-left': '30px', 'margin-right': "30px",
                    'margin-top': "10px"}
    ),

    dcc.Graph(
        id='box-graph',
        figure=box_fig
    ),
], style={'margin-left': '30px', 'margin-right': "30px", 'margin-top': "10px"})

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(
                "Exploratory analysis on how public transport use in London has "
                "changed due to the coronavirus pandemic",
                href="#"))
        ],
        brand="COMP0034: Coursework 1",
        brand_href="#",
        color="primary",
        dark=True,
        style={'height': '50px'}
    ),

    html.Div([html.Div('''There are many types of public transportation in London.
    In 2020, there were a lot of disruptions of Transport for London (TfL) because 
    of coronavirus pandemic. New regulations and changes led to the transition of 
    popularity for public transport journeys by type of transport. The following 
    visualisations are used to analyse the trends:''')],
             style={'margin-left': '30px', 'margin-right': "30px", 'margin-top': "10px"}),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Line graph', value='tab-1'),
        dcc.Tab(label='Bar chart', value='tab-2'),
        dcc.Tab(label='Pie chart', value='tab-3'),
        dcc.Tab(label='Subplots', value='tab-4'),
        dcc.Tab(label='Box plots', value='tab-5')],
             style={'textAlign': 'center',
                    'border': '2px solid indigo', 'margin-top': "10px"}),
    html.Div(id='tabs-content')

])


@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def changing_tabs(tab):
    """ Changing tabs function for callback

    Args:
        tab: user clicks on the tab

    Returns:
        tab: specific tab with the visualisation

    """
    if tab == 'tab-1':
        return line_graph_tab
    if tab == 'tab-2':
        return bar_graph_tab
    if tab == 'tab-3':
        return pie_chart_tab
    if tab == 'tab-4':
        return subplots_tab
    if tab == 'tab-5':
        return box_plots_tab

    return ''


@app.callback(
    Output(component_id='line-graph', component_property='figure'),
    Input(component_id='journey-types-dropdown', component_property='value'))
def update_line_graph(selected_type):
    """ Updating line graph

        Args:
            selected_type: a journey type chosen by the user

        Returns:
            line_fig_new: new line graph with only that journey type

        """
    if selected_type is not None:
        filtered_journeys = df[['Period ending', f'{selected_type}']]
        line_fig_new = px.line(filtered_journeys, x='Period ending',
                               y=f'{selected_type}',
                               title=f'Usage of {selected_type} in London')
    else:
        line_fig_new = line_fig
    return line_fig_new


@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='timeline-slider', component_property='value'))
def update_pie_graph(selected_year):
    """ Updating pie graph

        Args:
            selected_year: a timeline chosen by the user

        Returns:
            pie_fig_new: new pie graph with specific timeline

    """
    filtered_timeline = pd.DataFrame()
    if int(selected_year[1]) - int(selected_year[0]) == 1:
        for i in selected_year:
            filtered_timeline = filtered_timeline.append(
                df[df['Period ending'].astype(str).str.contains(f'{i}') == True])
    elif int(selected_year[1]) - int(selected_year[0]) == 2:
        selected_year.append(int(selected_year[1]) - 1)
        for i in selected_year:
            filtered_timeline = filtered_timeline.append(
                df[df['Period ending'].astype(str).str.contains(f'{i}') == True])
    elif int(selected_year[1]) - int(selected_year[0]) == 3:
        selected_year.append(int(selected_year[1]) - 1)
        selected_year.append(int(selected_year[1]) - 2)
        for i in selected_year:
            filtered_timeline = filtered_timeline.append(
                df[df['Period ending'].astype(str).str.contains(f'{i}') == True])
    elif int(selected_year[1]) == int(selected_year[0]):
        filtered_timeline = filtered_timeline.append(
            df[df['Period ending'].astype(str).str.contains(f'{selected_year[0]}') == True])
    pie_df_new = filtered_timeline[
        ['Bus journeys (m)', 'Underground journeys (m)', 'DLR journeys (m)', 'Tram journeys (m)',
         'Overground journeys (m)', 'Emirates Airline journeys (m)', 'TfL Rail journeys (m)']].sum()
    pie_fig_new = px.pie(values=pie_df_new.values, names=pie_df_new.index,
                         title="Amount of journeys in a year")
    return pie_fig_new


@app.callback(
    Output("box-graph", "figure"),
    Input("y-axis", "value"))
def update_box_plots(y_value):
    """ Updating box plots

        Args:
            y_value: a journey type chosen by the user

        Returns:
            box_fig_new: new box plot for only that journey type

    """
    box_fig_new = px.box(df, y=df[y_value])
    return box_fig_new


if __name__ == '__main__':
    app.run_server(debug=True)
