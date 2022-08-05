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
    return json['standings']['results']

# function that reurns each player current details using the player ID
def get_player_details(player_id):
    link = 'https://fantasy.premierleague.com/api/entry/' + str(player_id) + '/'
    page = requests.get(link)
    json = page.json()
    return json

# function that reurns each player history details using the player ID
def get_player_past_details(player_id):
    link = 'https://fantasy.premierleague.com/api/entry/' + str(player_id) + '/history/'
    page = requests.get(link)
    json = page.json()
    return json['current']

i=0
while (1):
    link = 'https://fantasy.premierleague.com/api/leagues-classic/' + league_number + '/standings?page_standings=' + str(i)
    try:
        table = table.append(get_table(link), ignore_index=True)
        i+= 1
    except:
        break

table.to_csv(str(date.today()) + ' current standings.csv', index=False)

player_list = list(table['entry'])


for player_id in player_list:
    player = get_player_details(player_id)
    player_table = player_table.append(player, ignore_index=True)
player_table.to_csv(str(date.today()) + ' players detail.csv', index=False)


for player_id in player_list:
    player_current = get_player_past_details(player_id)
    player_current_table = player_current_table.append(player_current, ignore_index=True)
player_current_table.to_csv(str(date.today()) + ' players past detail.csv', index=False)