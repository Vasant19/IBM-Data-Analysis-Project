import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

app = dash.Dash(__name__)

app.title = "Automobile Sales Statistics Dashboard"

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div([
    html.H1(children="Automobile Sales Statistics Dashboard", style={'textAlign': 'left', 'color': '#503D36', 'font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div(
        dcc.Dropdown(id='select-year', 
                   options=[{'label': i, 'value': i} for i in year_list],
                  placeholder='Select a year'
        )
    ),
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Automobile Sales during Recession Period"
            )
        )
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, 
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Expenditure Share by Vehicle Type during Recessions"
            )
        )
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart3)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart3)], style={'display': 'flex'})
        ]
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales"))
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicles Sold by Vehicle Type in the year {}".format(input_year)))
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart3)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart3)], style={'display': 'flex'})
        ]
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)