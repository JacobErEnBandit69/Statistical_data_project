# -*- coding: utf-8 -*-
"""
Created on Sun October 28 22:10:07 2020

@author: Jacob Kjaerager
"""

import datetime as dt
from dash.dependencies import Input, Output
import pandas as pd
import os
import socket
from pathlib import Path
import plotly.graph_objs as go
import dash
from callbacks import init_callback
from layout import layout
import psycopg2
import numpy as np
from DataLoader import get_data_from_uplink_db
import pytz

if __name__ == '__main__':

    app = dash.Dash(
           __name__,
           assets_folder="{}/styling".format(Path(__file__).parent)
          )

    app = layout(app)
    init_callback(app)
    print("{}/styling".format(Path(__file__).parent))

    app.run_server(host="0.0.0.0", debug=True, port=8050)


