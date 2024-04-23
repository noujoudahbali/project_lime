import pandas as pd 
import plotly.express as px
import geopandas as gpd

import boto3 
from dotenv import load_dotenv
import os 

import dash
from dash import html
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd


@callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    """
    Download the latest data from s3 and generates the figure """
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID') , aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    , region_name=os.environ.get('AWS_DEFAULT_REGION'))
    data_file = './data/bikes_data.csv'
    s3.download_file('lime-project','bikes_data.csv',data_file)

    bikes = pd.read_csv(data_file)
    bikes = bikes[['name','numbikesavailable','coordonnees_geo.lon','coordonnees_geo.lat']]
    fig = px.scatter_mapbox(bikes,
                            lat='coordonnees_geo.lat',
                            lon='coordonnees_geo.lon', 
                            hover_name="name", hover_data=['numbikesavailable'], 
                            color_discrete_sequence=["blue"])

    fig.update_layout(mapbox_style="open-street-map")
    return fig

# configure the dash app 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])# set app layout
app.layout = html.Div(children=[
    html.H1('Stations Lime', style={'textAlign':'center'}),
    html.Br(),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
            id='interval-component',
            interval=3600*1000, # in milliseconds - update every hour to update the graph ( the dag runs every hour too)
            n_intervals=0
        )
])
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, use_reloader=False)