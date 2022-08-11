import pandas as pd
import requests
from datetime import date
import os

table = pd.DataFrame()
player_table = pd.DataFrame()
player_current_table = pd.DataFrame()

# get the league number and number of players from the CSV File
league_number = '594384'


# create a folder for the reports if does not exist
try:
    os.chdir(os.getcwd() + '\\reports')
except:
    os.mkdir(os.getcwd() + '\\reports')
    os.chdir(os.getcwd() + '\\reports')


# function takes the url of the league number to retuen the league general info
def get_table(url):
    page = requests.get(url)
    json = page.json()
    return pd.json_normalize(json['standings']['results'])

# function that reurns each player current details using the player ID
def get_player_details(player_id):
    link = 'https://fantasy.premierleague.com/api/entry/' + str(player_id) + '/'
    page = requests.get(link)
    json = page.json()
    return pd.json_normalize(json)

# function that reurns each player history details using the player ID
def get_player_history_details(player_id):
    link = 'https://fantasy.premierleague.com/api/entry/' + str(player_id) + '/history/'
    page = requests.get(link)
    json = page.json()
    return pd.json_normalize(json['current'])

# get all the information from the API
# the current standing table is devided by pages.
i=1
while (1):
    link = 'https://fantasy.premierleague.com/api/leagues-classic/' + league_number + '/standings?page_standings=' + str(i)
    if len(get_table(link)): 
        table = pd.concat([table, get_table(link)], ignore_index=True)
        i+= 1
    else:
        break

player_list = list(table['entry'])

for player_id in player_list:
    player = get_player_details(player_id)
    player_table = pd.concat([player_table, player], ignore_index=True)

for player_id in player_list:
    player_current = get_player_history_details(player_id)
    player_current['id'] = [player_id] * len(player_current)
    player_current_table = pd.concat([player_current_table, player_current], ignore_index=True)


# rename and select only the columns that we need.
table.rename(columns = {'entry': 'ID', 'entry_name': 'team_name', 'event_total': 'week_points'}, inplace = True)
table = table[['ID', 'player_name', 'team_name', 'week_points', 'total', 'rank', 'last_rank', 'rank_sort']]
player_table.rename(columns= {'id': 'ID'}, inplace=True)

# merge both current_standing and player_table on 'ID'
table = pd.merge(table, player_table, how='outer', on='ID')

# save CSV files
table.to_csv(str(date.today()) + ' current standings.csv', index=False, encoding='utf_8_sig')
player_current_table.to_csv(str(date.today()) + ' players history detail.csv', index=False)