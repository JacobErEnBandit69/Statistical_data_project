# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:25:43 2020

@author: jacob
"""
import datetime as dt
from dash.dependencies import Input, Output
from api_handler import get_sport_data
import pandas as pd
import os
from pathlib import Path
import plotly.graph_objs as go

league_mapper = {
    "England_pl": "soccer_epl",
    "England_championship": "soccer_efl_champ",
    "Danish_superliga": 'soccer_denmark_superliga',
    "France_ligue1": "soccer_france_ligue_one",
    "Germany_bundesliga": "soccer_germany_bundesliga",
    "Holland_aeresdivision": "soccer_netherlands_eredivisie",
    "Norway_Eliteserien": "soccer_norway_eliteserien",
    "Portugal_primeira": "soccer_portugal_primeira_liga",
    "Russian_Pl": "soccer_russia_premier_league",
    "Spanish_laliga": "soccer_spain_la_liga",
    "Scottish_pl": "soccer_spl",
    "Swedish_allsvenskan": "soccer_sweden_allsvenskan",
    "Switzerland_superleague": "soccer_switzerland_superleague",
    "USA_MLS": "soccer_usa_mls",
}





CURRENT_SPORT = league_mapper["England_pl"]
print(CURRENT_SPORT)
def calculate_ttb(bet_one, bet_x, bet_two):
    
    return round((100 * 1/((1/bet_one)+(1/bet_x)+(1/bet_two))), 2)


def get_latest_data(df):
    q = []
    grouped_by_bookie = dict(list(df.groupby("bookmaker")))
        
    for i in grouped_by_bookie:
        q.append(grouped_by_bookie[i][grouped_by_bookie[i]["last_updated_bets"] == grouped_by_bookie[i]["last_updated_bets"].max()])
    filter_df = pd.concat(q)
    
    return filter_df.reset_index(drop=True)

def init_callback(app):   
    global df
    
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
        
        ###IMPORTANT TO CHANGE TO get_sport_data(CURRENT_SPORT) when deployed live
        
        global df
        df = get_sport_data(CURRENT_SPORT)
        
        options = [{'label': i, 'value': i} for i in sorted(list(df["matchname"].unique()))]
        value = next(iter(options))["label"]
        return "Data latest updated at: {}".format(time_now), options, value
    
    @app.callback(
        [
            Output(component_id ='datatable', component_property='columns'),
            Output(component_id ='datatable', component_property='data'),
            Output(component_id ='datatable', component_property='style_data_conditional'),
        ],
        [
            Input('dropdown_below_timestamp', 'value')
        ]
    )
    def update_table_data(dd_value):
        text_color = "black"
        background_color = 'rgb(67, 255, 86)'
        dd_filter = df[df["matchname"] == dd_value].drop(columns=["matchname"])
        filter_df = get_latest_data(dd_filter)
        filter_df["last_updated_bets"] = pd.to_datetime(filter_df["last_updated_bets"]).dt.strftime("%H:%M:%S  %d/%m/%Y")
        filter_df["time_of_match"] = pd.to_datetime(filter_df["time_of_match"]).dt.strftime("%H:%M:%S  %d/%m/%Y")
        columns=[{"name": i, "id": i} for i in filter_df.columns]
        data=filter_df.to_dict('records')
        conditional_style = [
                {
                    'if': {
                        'filter_query': '{{home}} = {}'.format(filter_df['home'].max()),
                        'column_id': 'home'
                    },
                    'backgroundColor': background_color,
                    'color': text_color
                },
                {
                    'if': {
                        'filter_query': '{{away}} = {}'.format(filter_df['away'].max()),
                        'column_id': 'away'
                    },
                    'backgroundColor': background_color,
                    'color': text_color
                },
                {
                    'if': {
                        'filter_query': '{{tie}} = {}'.format(filter_df['tie'].max()),
                        'column_id': 'tie'
                    },
                    'backgroundColor': background_color,
                    'color': text_color
                }
        ]
    
        return columns, data, conditional_style 
    
    @app.callback(
        [
            Output(component_id ='full_round_bar_chart', component_property='figure'),
        ],
        [
            Input(component_id ='dropdown_below_timestamp', component_property='value')
        ]
    )
    def update_graph_hometeam(dd_value):  
        global df
        match_grouped = dict(list(df.groupby("matchname")))
        data = []
        match_name = []
        TTB_index_hundered = []
        hovertext=[]
        color = []
        for i in match_grouped.keys():
            matches = match_grouped[i]
            max_ttb = calculate_ttb(matches["home"].max(), 
                                    matches["tie"].max(), 
                                    matches["away"].max()
                      )
            match_name.append(i)
            TTB_index_hundered.append(max_ttb-100)
            hovertext.append(max_ttb)
            if max_ttb > 100:
                color.append('rgb(67, 255, 86)')
            else: 
                color.append('rgb(236, 102, 102)')
            
            #maxes[i] = calculate_ttb(df["home"].max(), df["tie"].max(), df["away"].max())
        data=[
            go.Bar(
                x = match_name,
                y = TTB_index_hundered,
                hovertext = hovertext,
                marker_color= color,
            )
        ]
        fig = go.Figure(
                   data=data, 
               )
        fig.update_layout(
            title="Max available TTB with index 100 as 0",
            xaxis_title="Matches ",
            yaxis_title="Max TTB",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
            
                
        return [fig]
    
    @app.callback(
        [
            Output(component_id ='current_max_ttb', component_property='children'),
        ],
        [
            Input('dropdown_below_timestamp', 'value')
        ]
    )
    def update_data(dd_value):  
        match_grouped = df[df["matchname"] == dd_value].drop(columns=["matchname"])
        filter_df = get_latest_data(match_grouped)
        filter_df["last_updated_bets"] = pd.to_datetime(filter_df["last_updated_bets"]).dt.strftime("%H:%M:%S  %d/%m/%Y") 
        max_one = filter_df["home"].max()
        max_X = filter_df["tie"].max()
        max_two = filter_df["away"].max()
        max_ttb = calculate_ttb(max_one, max_X, max_two)
        
        return ["Max ttb: {} \nBets should be weighted: \n1: {}% \nX: {}% \n2: {}%".format(max_ttb, 
                                                                                            round((max_ttb/max_one), 3),
                                                                                            round((max_ttb/max_X), 3),
                                                                                            round((max_ttb/max_two), 3))]
    
    
    
    