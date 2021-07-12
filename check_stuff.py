import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    # Need to add bot activity


    print("ready")

@client.command()
async def ping(ctx):
    await ctx.send(f"Ping: {round(client.latency * 1000)} ms")

@client.command()
async def hello(ctx):
    # Accesses member object (in this case the author of the message) and sends them a DM while mentioning them
    await ctx.author.send(f'Hello {ctx.author}')
    print(ctx.author)

# @client.command()
# async def clear(ctx, amount=5):
#     # Purges last 5 messages in the channel
#     await ctx.channel.purge(limit=amount)

# @client.command()
# async def greet(ctx, greeting, *, name):
#     await ctx.send(f"{greeting}, {name}")

# @tasks.loop(seconds=2)
# async def message():
#     # Creates a loop that sends messages to a particular channel on 2 second intervals
#     await client.get_channel(752887027694960704).send("Hello")

# @client.command()
# async def nick(ctx, member: discord.Member, newname: str):
#     # Gets permissions that the message sender has
#     perms = ctx.channel.permissions_for(ctx.author)
#     if perms.manage_nicknames:
#         # If the sender can edit nicknames, edit
#         await member.edit(nick=newname)
#     else: 
#         await ctx.send("Don't  have necessary permissions")

# @client.command()
# async def role(ctx, member: discord.Member, role: discord.Role):
#     # Give the mentioned person a role
#     await member.add_roles(role)

# @client.event
# async def on_member_join(member):
#     await client.get_channel(752887027694960704).send(f"{member.mention} has joined!")

# @client.event
# async def on_member_remove(member):
#     await client.get_channel(752887027694960704).send(f"I hope {member} had fun!")

# @client.command()
# async def test(ctx, member: discord.Member):
#     await ctx.send(member.display_name) # first show with .nick

# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("Required arguments not given")

# @client.command(aliases=['embed'])
# async def test_embed(ctx):
#     embed = discord.Embed(title="Discord.py Workshop", color=discord.Color.green())
#     embed.add_field(name="Hello", value="Welcome to the Discord.py Workshop", inline=False)
#     embed.add_field(name="Instructor", value="Suhas Thalanki", inline=False)
#     #https://cog-creators.github.io/discord-embed-sandbox/
#     await ctx.send(embed=embed)


# Need to add embeds

client.run("ODQ4NTM5MjAwODE4NjQyOTQ1.YLOFtg._5QaUTQLnVL6BNNvvpPHgUiDbAI")