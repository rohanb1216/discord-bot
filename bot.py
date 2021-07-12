import discord
from discord.ext import commands, tasks
import requests
import sqlite3
import db_stuff

db_file = "d2.db"
conn = db_stuff.create_connection(db_file)

HEADERS = {"X-API-Key":'61a5a727617c492e9e3ce2e52bb3ca72'}




client  = commands.Bot(command_prefix = '!')



@client.command()
async def setusername(ctx, username:str):
    r = requests.get(f"https://www.bungie.net/platform/Destiny2/SearchDestinyPlayer/-1/{username}/", headers=HEADERS);
    userobject = r.json()
    if(userobject['Response'] != []):
        d2_id = userobject['Response'][0]['membershipId']
        discord_id = str(ctx.author)
        print(discord_id)
        d2_name = username
        ret = db_stuff.add_user(conn, discord_id, d2_name, d2_id)
        if(ret == True):
            await ctx.send(f"Verified and added {ctx.author.mention}")
        else:
            await ctx.send(f"{ctx.author.mention} already added")



@client.command()
async def last(ctx):
    uname = ctx.author
    ret = db_stuff.get_d2_member_id(ctx.author)
    memid = ret[1]
    

@client.command()
async def pvp_kd(ctx):
    uname = str(ctx.author)
    ret = db_stuff.get_d2_member_id(conn,uname)
    if(ret == ()):
        await ctx.send(f"User not added")
    else:
        memid = ret[1]
        Username = ret[0]
        statr = requests.get(f"https://www.bungie.net/platform/Destiny2/-1/Account/{memid}/Character/0/Stats", headers=HEADERS)
        statobject = statr.json()
        kd = statobject['Response']['allPvP']['allTime']['killsDeathsRatio']['basic']['displayValue']
        kda = statobject['Response']['allPvP']['allTime']['killsDeathsAssists']['basic']['displayValue']
        embed = discord.Embed(title=f"{Username}'s PvP stats:", color=discord.Color.green())
        embed.add_field(name="K/D", value=kd, inline=False)
        embed.add_field(name="KA/D", value=kda, inline=False)
        await ctx.send(embed=embed)

@client.command()
async def pvp_wep(ctx):
    uname = str(ctx.author)
    ret = db_stuff.get_d2_member_id(conn, uname)
    if(ret == ()):
        await ctx.send(f"User not added")
    else:
        Username = ret[0]
        memid = ret[1]
        statr = requests.get(f"https://www.bungie.net/platform/Destiny2/-1/Account/{memid}/Character/0/Stats", headers=HEADERS)
        statobject = statr.json()
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
        
        max = int(max)
        embed = discord.Embed(title=f"{Username}'s best PvP weapon:", color=discord.Color.green())
        embed.add_field(name="Weapon", value=max_name, inline=False)
        embed.add_field(name="Kills", value=max, inline=False)
        await ctx.send(embed=embed)



client.run("ODQ4NTM5MjAwODE4NjQyOTQ1.YLOFtg._5QaUTQLnVL6BNNvvpPHgUiDbAI")