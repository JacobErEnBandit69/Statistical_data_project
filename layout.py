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


def layout(app):
    app.layout = \
    html.Div(
        className="Full_view",
        children=[
            dcc.Interval(id='data_updater', interval=7200000 , n_intervals=0), 
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
                                        style_as_list_view=True,
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
            html.Div(
                className="left_half_of_view",
                children=[
                    html.Div(
                        className="card-background-dropdown-timestamp",
                        children=[
                            html.Div(
                                className="latest-update",
                                children = [
                                    html.Pre(id="latest_update"),
                                ]
                            ),
                            html.Div(
                                className="dropdown-below-timestamp",
                                children=[
                                    dcc.Dropdown(
                                        id='dropdown_below_timestamp',
                                        clearable=False
                                    )    
                                ],
                            ),
                        ]
                    ),
                    html.Div(
                        className="card-background-max-ttb",
                        children=[
                            html.Div(
                                className="ttb",
                                children=[
                                    html.H1(html.Pre(id="current_max_ttb")) 
                                ],
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
    return app