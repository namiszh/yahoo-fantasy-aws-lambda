#!/usr/bin/env python

import pandas as pd
from pandas import DataFrame
from scipy.stats import rankdata
import numpy as np



def data_to_ranking_score(values, reverse = False):
    '''
    Given a list of value, return a list of ranking score.
    If reverse = False, the biggest value will get the biggest ranking score.
    If reverse = True, the biggest value will get the smallest ranking score.
    Only category 'TO' should set 'reverse' to 'True'.

    The smallest ranking score is 1, the biggest ranking score is the element
    number of this list.
    '''
    scores = rankdata(values)
    if reverse:
        scores = [(len(values) + 1 - score) for score in scores]

    return scores

def stat_to_score(stat_df, sort_orders):
    '''Give then stats of a league for a week or the whole season, compute the ranking score
       sort_orders: {'FG%': '1', 'FT%': '1', '3PTM': '1', 'PTS': '1', 'OREB': '1', 'REB': '1', 'AST': '1', 'ST': '1', 'BLK': '1', 'TO': '0', 'A/T': '1'}
    '''
    score_df = stat_df.copy()

    for (stat_name, stat_value) in stat_df.items():
        sort_order = sort_orders[stat_name]

        reverse = (sort_order == '0')
        scores = data_to_ranking_score(stat_value.values, reverse)
        score_df[stat_name] = scores

    # add a column to display the total score of each team (row)
    score_df['Total'] = score_df.sum(axis=1)

    return score_df

def compute_battle_score(scores_team1, scores_team2):
    '''Given the category score of two players, compute the match up score between them
    '''
    a = 0
    b = 0
    for i in range(len(scores_team1) ):
        if (scores_team1[i] > scores_team2[i]):
            a += 1
        elif (scores_team1[i] < scores_team2[i]):
            b += 1
        else: 
            a += 0.5
            b += 0.5
    
    return a, b



def roto_score_to_battle_score(score_df, week_points):
    '''Give the roto score of a league for a week, calculate the matchup score against every other player
    '''

    battle_df = pd.DataFrame(columns=score_df.index, index=score_df.index) 

    # add a column named 'Ave' representing the average points he can get in this week
    # battle_df = battle_df.assign(AVE='NAN')
    # battle_df = battle_df.assign(DIF='NAN')

    team_scores = score_df.to_numpy()
    for i in range(len(team_scores) ):
        for j in range (i+1, len(team_scores)):
            score1, score2 = compute_battle_score(team_scores[i][:-1], team_scores[j][:-1])
            battle_df.iat[i, j] = score1
            battle_df.iat[j, i] = score2

    # calculate the median point a team can get
    battle_df['中位数'] = battle_df.median(axis=1)

    # the current point a team gets
    battle_df['本周得分'] = week_points

    # calculate the median point a team can get
    battle_df['分差'] = battle_df['本周得分'] - battle_df['中位数']

    final_df = battle_df.sort_values(by=['分差', '本周得分'], ascending=False)

    return final_df
            
