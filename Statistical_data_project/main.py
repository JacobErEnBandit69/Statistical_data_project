# -*- coding: utf-8 -*-
"""
Created on Sun October 28 22:10:07 2020

@author: Jacob Kjaerager
"""

import datetime as dt
from dash.dependencies import Input, Output
from api_handler import get_sport_data
import pandas as pd
import os
from pathlib import Path
import plotly.graph_objs as go
import dash
from callbacks import init_callback
from layout import layout

# An api key is emailed to you when you sign up to a plan
if __name__ == '__main__':
    
    app = dash.Dash(
           __name__,
           assets_folder="{}\styling".format(Path(__file__).parent)
          )
    
    app = layout(app)
    init_callback(app)
    app.run_server(debug=True)#host=socket.gethostbyname(socket.gethostname()), debug=True, port=4000)
    