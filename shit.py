import discord
from discord.ext import commands

client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():
    print("bot is ready")


def member_cleaner(lst):
    members_cleaned = []
    member_str = '' + str(lst)
    member_splitted = member_str.split('#')
    for x in range(0, int(len(member_splitted)),2):
        members_cleaned.append(member_splitted[x])
    return members_cleaned

@client.command()
async def test(ctx, *, member:discord.Member=None):
    await ctx.send(member.id)


client.run('NzI5MjI4NDk3NjY2NTcyMzYw.XwF49g.CgFbFirFkMFFqPkd4KcmW35G2eE')