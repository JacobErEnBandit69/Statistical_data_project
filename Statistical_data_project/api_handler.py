# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:08:36 2020

@author: jacob
"""


import requests
import json
import pandas as pd
import os
import pytz
from pathlib import Path

def calculate_ttb(bet_one, bet_x, bet_two):
    
    return round((100 * 1/((1/bet_one)+(1/bet_x)+(1/bet_two))), 2)

def get_differ_matrix(df):
    grouping_variable = "away_team"
    differ_matrix = df[["home", "tie", "away", grouping_variable]].groupby(grouping_variable).max() - \
       df[["home", "tie", "away", grouping_variable]].groupby(grouping_variable).min()
       
    print(calculate_ttb(differ_matrix["home"], differ_matrix["away"], differ_matrix["tie"]))
    
    return differ_matrix

def get_sport_data(sport_key):
    
    odds_response = \
    requests.get(url='https://api.the-odds-api.com/v3/odds', 
                 params={
                    'api_key': 'a3c9ca2eb4928f41bd56569ea7de1d97',
                    'sport': sport_key,
                    'region': 'eu', # uk | us | eu | au
                    'mkt': 'h2h' # h2h | spreads | totals
                 }
    )
    
    odds_json = json.loads(odds_response.text)
    
    ###Section intented for furture logging implementation###
    if not odds_json['success']:
        print(
            'There was a problem with the odds request:',
            odds_json['msg']
        )
    else:
        # Check your usage
        print('\nRemaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])
    ###Section intented for furture logging implementation###

    
   # df = pd.DataFrame(columns = ["home", "tie", "away", "home_team", "away_team",
    #                             "bookmaker", "row_ttb"])
    data = odds_json["data"]
    q = []
    for rows_of_data in range(len(data)):
        df = pd.DataFrame(columns = ["home", "tie", "away", "row_ttb", "home_team", "away_team",
                                 "bookmaker", "last_updated_bets", "matchname", "time_of_match"])
        match = data[rows_of_data]
        home =  match["home_team"]
        home_out_logic = [match['teams'][0], match['teams'][1]]
        match['teams'].remove(home)
        away =  match['teams'][0]
        for i in range(len(match['sites'])):
            h2h = match['sites'][i]["odds"]["h2h"]
            if home_out_logic[0] == home:
                df.loc[rows_of_data*i + i, "home"] = h2h[0]
                df.loc[rows_of_data*i + i, "away"] = h2h[1]
            else: 
                df.loc[rows_of_data*i + i, "home"] = h2h[1]
                df.loc[rows_of_data*i + i, "away"] = h2h[0]
                
            df.loc[rows_of_data*i + i, "time_of_match"] = pd.to_datetime(data[rows_of_data]["commence_time"], unit="s")
            df.loc[rows_of_data*i + i, "tie"] = h2h[2]    
            df.loc[rows_of_data*i + i, "home_team"] = home
            df.loc[rows_of_data*i + i, "away_team"] = away
            df.loc[rows_of_data*i + i, "bookmaker"] = match['sites'][i]['site_nice']
            df.loc[rows_of_data*i + i, "row_ttb"] = calculate_ttb(h2h[0], h2h[1], h2h[2])
            df.loc[rows_of_data*i + i, "last_updated_bets"] = pd.to_datetime(
                                                                  match['sites'][i]["last_update"],
                                                                  unit="s"
                                                              ).tz_localize("UTC").tz_convert("Europe/Copenhagen")
            df.loc[rows_of_data*i + i, "matchname"] = "{} - {}".format(home,  away)
            
        q.append(df)
    df = pd.concat(q).reset_index(drop=True)
    
    storage_file = "./historical_data/datafile.pkl"    
    former_df = [pd.read_pickle(storage_file), df]
    
    df_total = pd.concat(former_df).drop_duplicates().reset_index(drop=True)
    pd.to_pickle(df_total, storage_file) #Save a copy for future to historical analysis
    
    return df


if __name__ == '__main__': 
    sport_key = "soccer_epl"
    df = get_sport_data(sport_key)