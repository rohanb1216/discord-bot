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

hashes = {
'DestinyAchievementDefinition':'hash',                
'DestinyActivityDefinition':'hash',                   
'DestinyActivityGraphDefinition':'hash',              
'DestinyActivityModeDefinition':'hash',               
'DestinyActivityModifierDefinition':'hash',           
'DestinyActivityTypeDefinition':'hash',               
'DestinyArtifactDefinition':'hash',                   
'DestinyBondDefinition':'hash',                       
'DestinyBreakerTypeDefinition':'hash',                
'DestinyChecklistDefinition':'hash',                  
'DestinyClassDefinition':'hash',                      
'DestinyCollectibleDefinition':'hash',                
'DestinyDamageTypeDefinition':'hash',                 
'DestinyDestinationDefinition':'hash',                
'DestinyEnergyTypeDefinition':'hash',                 
'DestinyEquipmentSlotDefinition':'hash',              
'DestinyFactionDefinition':'hash',                    
'DestinyGenderDefinition':'hash',                     
'DestinyHistoricalStatsDefinition':'statId',            
'DestinyInventoryBucketDefinition':'hash',            
'DestinyInventoryItemDefinition':'hash',              
'DestinyItemCategoryDefinition':'hash',               
'DestinyItemTierTypeDefinition':'hash',               
'DestinyLocationDefinition':'hash',                   
'DestinyLoreDefinition':'hash',                       
'DestinyMaterialRequirementSetDefinition':'hash',     
'DestinyMedalTierDefinition':'hash',                  
'DestinyMetricDefinition':'hash',                     
'DestinyMilestoneDefinition':'hash',                  
'DestinyObjectiveDefinition':'hash',                  
'DestinyPlaceDefinition':'hash',                      
'DestinyPlugSetDefinition':'hash',                    
'DestinyPowerCapDefinition':'hash',                   
'DestinyPresentationNodeDefinition':'hash',           
'DestinyProgressionDefinition':'hash',                
'DestinyProgressionLevelRequirementDefinition':'hash',
'DestinyRaceDefinition':'hash',                       
'DestinyRecordDefinition':'hash',                     
'DestinyReportReasonCategoryDefinition':'hash',       
'DestinyRewardSourceDefinition':'hash',               
'DestinySackRewardItemListDefinition':'hash',         
'DestinySandboxPatternDefinition':'hash',             
'DestinySandboxPerkDefinition':'hash',                
'DestinySeasonDefinition':'hash',                     
'DestinySeasonPassDefinition':'hash',                 
'DestinySocketCategoryDefinition':'hash',             
'DestinySocketTypeDefinition':'hash',                 
'DestinyStatDefinition':'hash',                       
'DestinyStatGroupDefinition':'hash',                  
'DestinyTalentGridDefinition':'hash',                 
'DestinyTraitCategoryDefinition':'hash',              
'DestinyTraitDefinition':'hash',                      
'DestinyUnlockDefinition':'hash',                     
'DestinyVendorDefinition':'hash',                     
'DestinyVendorGroupDefinition':'hash',      
}

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


def get_manifest():
    manifest_url = 'http://www.bungie.net/Platform/Destiny2/Manifest/'

    #get the manifest location from the json
    r = requests.get(manifest_url, headers=HEADERS)
    manifest = r.json()
    mani_url = 'http://www.bungie.net'+manifest['Response']['mobileWorldContentPaths']['en']

    #Download the file, write it to 'MANZIP'
    r = requests.get(mani_url)
    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    #Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    os.rename(name[0], 'manifest.content')
    print('Unzipped!')


def build_dict(hash_dict):
    #connect to the manifest
    con = sqlite3.connect('manifest.content')
    print('Connected')
    #create a cursor object
    cur = con.cursor()

    all_data = {}
    #for every table name in the dictionary
    for table_name in hash_dict.keys():
        #get a list of all the jsons from the table
        cur.execute('SELECT json from '+table_name)
        print('Generating '+table_name+' dictionary....')

        #this returns a list of tuples: the first item in each tuple is our json
        items = cur.fetchall()

        #create a list of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        #create a dictionary with the hashes as keys
        #and the jsons as values
        item_dict = {}
        hash = hash_dict[table_name]
        # print()
        for item in item_jsons:
            # pprint(item)
            item_dict[item[hash]] = item

        #add that dictionary to our all_data using the name of the table
        #as a key.
        all_data[table_name] = item_dict

    print('Dictionary Generated!')
    return all_data
#check if pickle exists, if not create one.
if os.path.isfile(r'manifest.content') == False:
    get_manifest()
    all_data = build_dict(hashes)
    with open('manifest.pickle', 'wb') as data:
        pickle.dump(all_data, data)
        print("'manifest.pickle' created!\nDONE!")
else:
    print('Pickle Exists')

with open('manifest.pickle', 'rb') as data:
    all_data = pickle.load(data)




username = input('Enter Destiny Username: ')

u = requests.get(f"https://www.bungie.net/platform/Destiny2/SearchDestinyPlayer/-1/{username}/", headers=HEADERS)

userobject = u.json()
if(userobject['Response'] != []):
    d2_id = userobject['Response'][0]['membershipId']

# print(jsonobj)
maxref = 0
maxkills = 0
valarray = []

# sort by weapon kills
w = requests.get(f"https://www.bungie.net/platform/Destiny2/-1/Account/{d2_id}/Character/0/Stats/UniqueWeapons", headers=HEADERS)
jsonobj = w.json()
jsonobj = jsonobj['Response']


for i in jsonobj['weapons']:

    kills = i['values']['uniqueWeaponKills']['basic']['value'] 
    print(all_data['DestinyInventoryItemDefinition'][i['referenceId']])
    # r = requests.get(f"https://bungie.net/platform/Destiny2/Manifest/DestinyInventoryItemDefinition/{i['referenceId']}/", headers=HEADERS)
    # resobj = r.json()


    # if(resobj['Response']['displayProperties']['hasIcon']):
    #     iconpath = 'https://bungie.net/'+resobj['Response']['displayProperties']['icon']
    # wepname = resobj['Response']['displayProperties']['name']
    


    iconpath = all_data['DestinyInventoryItemDefinition'][i['referenceId']]['']
    wepname = all_data['DestinyInventoryItemDefinition'][i['referenceId']]

    valarray.append({'referenceId':i['referenceId'], 'uniqueWeaponKills':kills, 'iconpath':iconpath, 'name':wepname})
    if(kills>maxkills):
        maxkills = kills
        maxref = i['referenceId']
    # time.sleep(5)

print(len(valarray))

valarray = sorted(valarray, key=itemgetter('uniqueWeaponKills'), reverse=True)

f = open('resjson.json', 'w+')
json.dump(valarray, f)
f.close()

df = pd.DataFrame(valarray)

# HTML(df.to_html(escape=False, formatters=dict(iconpath=path_to_image_html)))

df.to_html('res.HTML', escape=False, formatters=dict(iconpath=path_to_image_html))

print(df)


print('maxref:', maxref )
print('maxkills:', maxkills)
# print(valarray)




