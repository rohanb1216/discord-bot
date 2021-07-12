import requests

HEADERS = {"X-API-Key":'61a5a727617c492e9e3ce2e52bb3ca72'}


r = requests.get(f"https://www.bungie.net/platform/Destiny2/SearchDestinyPlayer/-1/doctorzeuss77/", headers=HEADERS);
userobject = r.json()
# print(userobject)
# print(userobject['Response'][0])
memid = userobject['Response'][0]['membershipId']

# print(memid)


statr = requests.get(f"https://www.bungie.net/platform/Destiny2/-1/Account/{memid}/Character/0/Stats", headers=HEADERS)

statobject = statr.json()

print(statobject)

kd = statobject['Response']['allPvP']['allTime']['killsDeathsRatio']['basic']['displayValue']
kda = statobject['Response']['allPvP']['allTime']['killsDeathsAssists']['basic']['displayValue']

print(kd, kda)

weapon_stats = {}
for i in statobject['Response']['allPvP']['allTime'].keys():
    if('weaponKills' in i):
        weapon_stats[i[11:]] = statobject['Response']['allPvP']['allTime'][i]["basic"]["value"]

max = -1
max_name = ""
for i in weapon_stats.keys():
    if(weapon_stats[i] > max):
        max = weapon_stats[i]
        max_name = i

print(max_name)
print(max)