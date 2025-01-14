import requests
import json



def get_players(players_ids):
    players = []

    for player_id in players_ids:
        url = f'http://localhost:8000/players/{player_id}/profile'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error getting player with id {player_id}')
            continue

        player_info = response.json()

        player = {
            'id': player_info['id'],
            'name': player_info['name'],
            'url': player_info['url'],
            'imageUrl': player_info['imageUrl'],
        }

        players.append(player)

    return players


#read the players_ids from the players_ids.json file
with open('players_ids.json', 'r') as file:
    players_ids = json.load(file)

# Get players from the players ids
players = get_players(players_ids)

# Save the players in a json file
with open('players.json', 'w') as file:
    json.dump(players, file)