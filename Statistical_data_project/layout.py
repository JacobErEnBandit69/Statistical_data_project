# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:06:24 2020

@author: Jacob Kjaerager
"""

import dash
import dash_table
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

def get_hour_selector_options():
    options = [i for i in range(0,24)]
    options.insert("all_data", 0)
    return 

def layout(app):
    app.layout = \
    html.Div(
        className="Full_view",
        children=[
            html.Div(id="dummy_id_for_default"),
            dcc.Interval(id='data_updater', interval=60000 , n_intervals=0), 
            html.Div(
                className="left_half_of_view",
                children=[
                    html.Div(
                        className="card-background-dropdown-timestamp",
                        children=[
                            html.Div(
                                className="dropdown-below-timestamp",
                                children=[
                                    html.H4(html.Pre(id="latest_update")),
                                    html.Pre("Pick a gateway"),
                                    dcc.Dropdown(
                                        id='dropdown_below_timestamp',
                                        clearable=False
                                    )
                                ],
                            ),
                            html.Div(
                                className="datepicker",
                                children=[
                                    html.Pre("Pick a date:"),
                                    dcc.DatePickerRange(
                                        id='datepicker',
                                    )
                                ],
                            ),
                            html.Div(
                                className="hour-selector",
                                children=[
                                    html.Pre("Pick a specific interval:"),
                                    dcc.Dropdown(
                                        id='hour_selector',
                                        multi=True,
                                        clearable=True,
                                        options = [i for i in range(0,24)],
                                    )
                                ],
                            ),
                        ]
                    ),
                    html.Div(
                        className="card-background-circular-graph",
                        children=[
                            html.Div(
                                className="circular-pie-chart",
                                children=[
                                    dcc.Graph(
                                        id="gps_success_circular_graph"
                                    )
                                ],
                            ),
                        ],
                    ),
                ]
            ),
            html.Div(
                className="right_side_of_view",
                children=[
                    html.Div(
                        className="card-datatable-ttb",
                        children=[
                            html.Div(
                                className="datatable",
                                children=[
                                    dash_table.DataTable(
                                        id='datatable',
                                        #style_as_list_view=True,
                                        fixed_rows={
                                            'headers': True
                                        },
                                        style_table={
                                            'height': 400,
                                            'overflowX': 'auto',
                                        },
                                        style_cell={
                                            'textAlign': 'center',
                                            'overflow': 'hidden',
                                            'minWidth': '80px',
                                            'width': '80px',
                                            'maxWidth': '180px',
                                        }
                                    )
                                ],
                            ),
                        ]
                    ),
                    html.Div(
                        className="graph-card",
                        children=[
                            html.Div(
                                className="historical-graph-odds-development-hometeam",
                                children=[
                                    dcc.Graph(
                                        id="full_round_bar_chart"
                                    )
                                ]
                            )
                        ]
                    )
                ],
            ),
        ]
    )
    return app
