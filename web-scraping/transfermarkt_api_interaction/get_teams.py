import requests
import json

LEAGUE_ID = "GB1"

def get_teams(league_id):
    url = f'http://localhost:8000/competitions/{league_id}/clubs'

    response = requests.get(url)

    if response.status_code != 200:
        return []
    

    teams_info = response.json()

    teams_id = [team['id'] for team in teams_info['clubs']]

    return teams_id


#Save the teams in a json file
with open('teams.json', 'w') as file:
    json.dump(get_teams(LEAGUE_ID), file)




