# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:25:43 2020

@author: jacob
"""
import datetime as dt
from dash.dependencies import Input, Output
import pandas as pd
import os
from pathlib import Path
import plotly.graph_objs as go
from DataLoader import get_data_from_uplink_db



class DataObject:

    def __init__(self):
        self.full_uplink_data = get_data_from_uplink_db()




def init_callback(app):

    do = DataObject()

    @app.callback(
        [
            Output(component_id ='latest_update', component_property='children'),
            Output(component_id ='dropdown_below_timestamp', component_property='options'),
            Output(component_id ='dropdown_below_timestamp', component_property='value'),
        ],
        [
            Input('data_updater', 'n_intervals')
        ]
    )
    def update_all_data(n):
        time_now = dt.datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
        do.full_uplink_data = get_data_from_uplink_db()
        df = do.full_uplink_data
        print(df["gateway_name"].unique())
        options = [{'label': i, 'value': i} for i in sorted(list(df["gateway_name"].unique()))]
        options.append({"label": "all data", "value": "all_data"})
        value = next(iter(options))["value"]
        return "Data latest updated at: {}".format(time_now), options, value

    @app.callback(
        [
            Output(component_id ='datatable', component_property='columns'),
            Output(component_id ='datatable', component_property='data'),
        ],
        [
            Input('dropdown_below_timestamp', 'value')
        ]
    )
    def update_table_data(dd_value):
        text_color = "black"
        background_color = 'rgb(67, 255, 86)'
        df = do.full_uplink_data
        df = df[df["tx_latitude"] != 0]
        if dd_value != "all_data":
            df = df[df["gateway_name"] == dd_value]
        columns=[{"name": i, "id": i} for i in df.columns]
        data=df.to_dict('records')

        return columns, data

    @app.callback(
        [
            Output(component_id ='full_round_bar_chart', component_property='figure'),
        ],
        [
            Input(component_id ='dropdown_below_timestamp', component_property='value')
        ]
    )
    def update_graph_hometeam(dd_value):
        df = do.full_uplink_data
        df = df[df["tx_latitude"] != 0]
        if dd_value != "all_data":
            df = df[df["gateway_name"] == dd_value]

        mapbox_access_token = "pk.eyJ1IjoiamFjb2I3NCIsImEiOiJjazhzcW9peXgwMjF2M21wOGdxenozMWRpIn0.cvEeafk5_3_FS-zkcOE6Jw"
        data=[
            go.Scattermapbox(
                mode="markers",
                lat = df["tx_latitude"],
                lon = df["tx_longitude"],
                hovertext = df["rssi"],
                marker=go.scattermapbox.Marker(
                    size=11,
                    color=df["rssi"],
                    colorbar=dict(
                        title="Rssi"
                    ),
                    colorscale="Jet",
                )
            ),
        ]
        fig = go.Figure(
                   data=data,
               )
        fig.update_layout(
            title="Map for endpoint with GPS enabled",
            autosize=True,
            hovermode='closest',
            showlegend = False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict( #Center of map
                    lat = 56.155737,
                    lon = 10.189122,
                ),
                pitch=0,
                zoom=16,
            ),
            legend_title="RSSI for endpoints",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        return [fig]



