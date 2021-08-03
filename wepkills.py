import json
from operator import itemgetter
import requests
import time
import pandas as pd
from IPython.core.display import HTML
import os, pickle, sqlite3, zipfile
from pprint import pprint

authorize_url='https://www.bungie.net/en/oauth/authorize'
token_url='https://www.bungie.net/platform/app/oauth/token/'

hashes_trunc = {
    'DestinyInventoryItemDefinition': 'itemHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyStatGroupDefinition': 'statGroupHash'
}


HEADERS = {"X-API-Key":'61a5a727617c492e9e3ce2e52bb3ca72'}

# f = open('weaponkills.json', 'r')

# f.close()

def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'

with open('manifest.pickle', 'rb') as data:
    all_data = pickle.load(data)




username = input('Enter Destiny Username: ')

u = requests.get(f"https://www.bungie.net/platform/Destiny2/SearchDestinyPlayer/-1/{username}/", headers=HEADERS)

resobject = u.json()
if(resobject['Response'] != []):
    d2_id = resobject['Response'][0]['membershipId']

# print(jsonobj)
maxref = 0
maxkills = 0
valarray = []

# sort by weapon kills
w = requests.get(f"https://www.bungie.net/platform/Destiny2/-1/Account/{d2_id}/Character/0/Stats/UniqueWeapons", headers=HEADERS)
resobj = w.json()
resobj = resobj['Response']


for i in resobj['weapons']:

    kills = i['values']['uniqueWeaponKills']['basic']['value'] 
    # pprint(all_data['DestinyInventoryItemDefinition'][i['referenceId']])
    

    if(all_data['DestinyInventoryItemDefinition'][i['referenceId']]['displayProperties']['hasIcon']):
        iconpath = 'https://bungie.net/'+all_data['DestinyInventoryItemDefinition'][i['referenceId']]['displayProperties']['icon']
    wepname = all_data['DestinyInventoryItemDefinition'][i['referenceId']]['displayProperties']['name']

    valarray.append({'referenceId':i['referenceId'], 'name':wepname, 'Kills':kills, 'icon':iconpath})
    if(kills>maxkills):
        maxkills = kills
        maxref = i['referenceId']
    # time.sleep(5)

print(len(valarray))

valarray = sorted(valarray, key=itemgetter('Kills'), reverse=True)


df = pd.DataFrame(valarray)

# HTML(df.to_html(escape=False, formatters=dict(iconpath=path_to_image_html)))

df.to_html('res.HTML', escape=False, formatters=dict(iconpath=path_to_image_html))

print(df)


print('maxref:', maxref )
print('maxkills:', maxkills)
# print(valarray)




