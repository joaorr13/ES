import requests
import json


def get_players_ids(teams_ids):
    players_ids = []
    for team_id in teams_ids:
        url = f'http://localhost:8000/clubs/{team_id}/players'
        response = requests.get(url)
        if response.status_code != 200:
            return []
        players_info = response.json()

        players_ids += [player['id'] for player in players_info['players']]

    return players_ids

#read the teams_ids from the teams.json file
with open('teams.json', 'r') as file:
    teams_ids = json.load(file)

# Get players ids from the teams ids
players_ids = get_players_ids(teams_ids)

# Save the players ids in a json file
with open('players_ids.json', 'w') as file:
    json.dump(players_ids, file)