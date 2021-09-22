#Ottawa League Scraper Tool
#This tool will be used to extract data from the yahoo fantasy "Ottawa League", making use of the Fantasy Sports API

import logging
import os
import pprint
import warnings
import pprint
import json
import pandas as pd
import pytest
import requests
import openpyxl
from dotenv import load_dotenv

from yfpy import Data
from yfpy.models import Game, StatCategories, User, Scoreboard, Settings, Standings, League, Player, Team,TeamPoints, TeamStandings, Roster
from yfpy.query import YahooFantasySportsQuery

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)

# load python-dotenv to parse environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path=env_path)
print(env_path)

# Turn on/off example code stdout printing output
print_output = True

# Turn on/off automatic opening of browser window for OAuth
browser_callback = True

# Put private.json (see README.md) in test/ directory
auth_dir = "C:\\Users\\Joshua\\Desktop\\Ottawa League Scraper"

teamInfo = []

# Example code will output data here
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output")
print(data_dir)

# Test vars
chosen_week = 1
chosen_date = "2019-10-15"  # NHL

team_name = "Malkin in the Middle"

league_id = "41827" #corresponds to 2020 season
league_id_2019 = "5132" #corresponds to 2019 season

# Instantiate yfpy query object
yahoo_data = Data(data_dir)
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id_2019,
    game_id = 396,
    game_code= "nhl",
    offline= False,
    all_output_as_json= False,
    consumer_key="enter key",
    consumer_secret="enter secret",
    browser_callback=browser_callback
)

### USE THIS TO FIND INFO ABOUT PREVIOUS YEARS ###
#print(yahoo_query.get_user_teams())

### Get relevant keys for specific season  ###
# league_key= yahoo_query.get_league_key(season=2020)
# print(league_key)

### Analyzing 2019 data ###
#objective: see which team performed best in each category for a given week

#initialize empty df to hold stats
df = pd.DataFrame()

league_info = yahoo_query.get_game_info_by_game_id(396)
# columns = ["Player Name","Fantasy Team","position"]

# for stats in league_info.stat_categories.stats:
#     columns.append(stats['stat'].name)


# print(league_info.stat_categories.stats)
# test = yahoo_query.get_team_info(2)
# print(test)
# print(test.roster.players[16]['player'].selected_position_value)

allData = []

for team_id in range(1,13):
    team = yahoo_query.get_team_info(team_id)
    # teamName = str(team.name)[2:-1]     #pull fantasy team name

    for player in team.roster.players:
        fantasyPlayer = [] #to hold all stats pulled with yfpy on a team-by-team basis
        fantasyPlayer.append(str(team.name)[2:-1]) #add the fantasy team owner for each player
        fantasyPlayer.append(player['player'].name.full) #collecting each player's full name
        fantasyPlayer.append(player['player'].display_position)

        #collecting player's stats for given week
        # player_key = player['player'].player_key
        # playerData = yahoo_query.get_player_stats_for_season(player_key)
        # print(playerData)


        # print(fantasyPlayer)
        #append this player's data to the dataframe
        allData.append(fantasyPlayer)


df = pd.DataFrame(allData, columns=columns)
stat_ids = pd.DataFrame(stat_ids)

with pd.ExcelWriter('test yfpy.xlsx') as writer:
    df.to_excel(writer, sheet_name = "teams", engine = 'openpyxl')
    stat_ids.to_excel(writer, sheet_name = "stat_ids", engine = 'openpyxl')

print("done")
