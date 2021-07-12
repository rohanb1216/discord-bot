import os, pickle, sqlite3, zipfile, json, requests
from pprint import pprint

hashes = {
    "DestinyAchievementDefinition": "hash",
    "DestinyActivityDefinition": "hash",
    "DestinyActivityGraphDefinition": "hash",
    "DestinyActivityModeDefinition": "hash",
    "DestinyActivityModifierDefinition": "hash",
    "DestinyActivityTypeDefinition": "hash",
    "DestinyArtifactDefinition": "hash",
    "DestinyBondDefinition": "hash",
    "DestinyBreakerTypeDefinition": "hash",
    "DestinyChecklistDefinition": "hash",
    "DestinyClassDefinition": "hash",
    "DestinyCollectibleDefinition": "hash",
    "DestinyDamageTypeDefinition": "hash",
    "DestinyDestinationDefinition": "hash",
    "DestinyEnergyTypeDefinition": "hash",
    "DestinyEquipmentSlotDefinition": "hash",
    "DestinyFactionDefinition": "hash",
    "DestinyGenderDefinition": "hash",
    "DestinyHistoricalStatsDefinition": "statId",
    "DestinyInventoryBucketDefinition": "hash",
    "DestinyInventoryItemDefinition": "hash",
    "DestinyItemCategoryDefinition": "hash",
    "DestinyItemTierTypeDefinition": "hash",
    "DestinyLocationDefinition": "hash",
    "DestinyLoreDefinition": "hash",
    "DestinyMaterialRequirementSetDefinition": "hash",
    "DestinyMedalTierDefinition": "hash",
    "DestinyMetricDefinition": "hash",
    "DestinyMilestoneDefinition": "hash",
    "DestinyObjectiveDefinition": "hash",
    "DestinyPlaceDefinition": "hash",
    "DestinyPlugSetDefinition": "hash",
    "DestinyPowerCapDefinition": "hash",
    "DestinyPresentationNodeDefinition": "hash",
    "DestinyProgressionDefinition": "hash",
    "DestinyProgressionLevelRequirementDefinition": "hash",
    "DestinyRaceDefinition": "hash",
    "DestinyRecordDefinition": "hash",
    "DestinyReportReasonCategoryDefinition": "hash",
    "DestinyRewardSourceDefinition": "hash",
    "DestinySackRewardItemListDefinition": "hash",
    "DestinySandboxPatternDefinition": "hash",
    "DestinySandboxPerkDefinition": "hash",
    "DestinySeasonDefinition": "hash",
    "DestinySeasonPassDefinition": "hash",
    "DestinySocketCategoryDefinition": "hash",
    "DestinySocketTypeDefinition": "hash",
    "DestinyStatDefinition": "hash",
    "DestinyStatGroupDefinition": "hash",
    "DestinyTalentGridDefinition": "hash",
    "DestinyTraitCategoryDefinition": "hash",
    "DestinyTraitDefinition": "hash",
    "DestinyUnlockDefinition": "hash",
    "DestinyVendorDefinition": "hash",
    "DestinyVendorGroupDefinition": "hash",
}

HEADERS = {"X-API-Key": "61a5a727617c492e9e3ce2e52bb3ca72"}


def get_manifest():
    manifest_url = "http://www.bungie.net/Platform/Destiny2/Manifest/"

    # get the manifest location from the json
    r = requests.get(manifest_url, headers=HEADERS)
    manifest = r.json()
    mani_url = (
        "http://www.bungie.net" + manifest["Response"]["mobileWorldContentPaths"]["en"]
    )

    # Download the file, write it to 'MANZIP'
    r = requests.get(mani_url)
    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    # Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile("MANZIP") as zip:
        name = zip.namelist()
        zip.extractall()
    os.rename(name[0], "manifest.content")
    print("Unzipped!")


def build_dict(hash_dict):
    # connect to the manifest
    con = sqlite3.connect("manifest.content")
    print("Connected")
    # create a cursor object
    cur = con.cursor()

    all_data = {}
    # for every table name in the dictionary
    for table_name in hash_dict.keys():
        # get a list of all the jsons from the table
        cur.execute("SELECT json from " + table_name)
        print("Generating " + table_name + " dictionary....")

        # this returns a list of tuples: the first item in each tuple is our json
        items = cur.fetchall()

        # create a list of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        # create a dictionary with the hashes as keys
        # and the jsons as values
        item_dict = {}
        hash = hash_dict[table_name]
        # print()
        for item in item_jsons:
            # pprint(item)
            item_dict[item[hash]] = item

        # add that dictionary to our all_data using the name of the table
        # as a key.
        all_data[table_name] = item_dict

    print("Dictionary Generated!")
    return all_data


# check if pickle exists, if not create one.
if os.path.isfile(r"manifest.content") == False:
    get_manifest()
    all_data = build_dict(hashes)
    with open("manifest.pickle", "wb") as data:
        pickle.dump(all_data, data)
        print("'manifest.pickle' created!\nDONE!")
else:
    print("Pickle Exists")
