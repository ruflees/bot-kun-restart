import discord
import datetime
from discord import Embed
from discord.ext import commands

client = commands.Bot(command_prefix='b:')
client.remove_command('help')

@client.event
async def on_ready():
    print("bot is ready")


@client.command()
async def ping(ctx):
    await ctx.send("pong")
    print(ctx.author)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


#voting-----------------------------------
vote_start = False
separated_vote = False
fase_2 = False
dict_for_voting = {}
voters = {}
winner = {}

#starts a voting session-----------------------------------------------
@client.command()
@commands.has_role('Bartender')
async def start(ctx, arg="off"):
    global vote_start, separated_vote
    if vote_start == False:
        if arg.lower() == "on":
            separated_vote = False
            await ctx.send('A separated voting session has been started, please add your contenders.')
            vote_start = False
            print("A voting session has been started")

            x = datetime.datetime.now()
            contenders_file = open("data/contenders.txt", "a")
            voters_file = open("data/voters.txt", "a")
            contenders_file.write(" # %s/%s/%s&: "%(x.strftime("%d"), x.strftime("%m"), x.strftime("%Y")))
            voters_file.write(" # %s/%s/%s&: "%(x.strftime("%d"), x.strftime("%m"), x.strftime("%Y")))
            contenders_file.close()
            voters_file.close()

        elif arg.lower() == "off":
            await ctx.send('A voting session has been started, please add your contenders.')
            vote_start = False
            print("A voting session has been started")

            x = datetime.datetime.now()
            contenders_file = open("data/contenders.txt", "a")
            voters_file = open("data/voters.txt", "a")
            contenders_file.write(" # %s/%s/%s&: "%(x.strftime("%d"), x.strftime("%m"), x.strftime("%Y")))
            voters_file.write(" # %s/%s/%s&: "%(x.strftime("%d"), x.strftime("%m"), x.strftime("%Y")))
            contenders_file.close()
            voters_file.close()

    elif vote_start == False:
        if separated_vote == False:
            await ctx.send('The separated voting session has already been started.')
        elif separated_vote == False:
            await ctx.send('The voting session has already been started.')


#stops the voting session------------------------------------------------------
@client.command()
@commands.has_role('Bartender')
async def stop(ctx):
    global vote_start, fase_2
    if vote_start == False:
        await ctx.send("The voting session has been ended.")
        vote_start = False
        fase_2 = False
        print("A voting session has been ended.")
    else:
        await ctx.send('There is no voting session in progress.')


#creates a contender called in by the author------------------------------------------
@client.command()
async def add(ctx, *, name):
    global dict_for_voting
    name_checker = [dict_for_voting[x][0].lower() for x in dict_for_voting]
    if vote_start != False:
        await ctx.send("There is no voting session in progress.")

    elif str(name.lower()) in name_checker:
        await ctx.send("A contender with the same name has already been added.")

    else:
        if separated_vote == False and fase_2 == False:
            await ctx.send("%s the contender adding fase is already done."%ctx.author.mention)

        elif separated_vote == False and fase_2 == False:
            await ctx.send("%s added %s" %(ctx.author.name, name))
            dict_for_voting.update({ctx.author.id : [str(name), str(ctx.author.nick), 0, str(ctx.author.id)]})

            contenders_file = open("contenders.txt", "a")
            contenders_file.write("%s, %s, %s; " %(str(name), str(ctx.author.nick), str(ctx.author.id)))
            contenders_file.close()

            print(dict_for_voting)

        else:
            await ctx.send("%s added %s" %(ctx.author.name, name))
            dict_for_voting.update({ctx.author.id : [str(name), str(ctx.author.nick), 0, str(ctx.author.id)]})

            contenders_file = open("contenders.txt", "a")
            contenders_file.write("%s, %s, %s; " %(str(name), str(ctx.author.nick), str(ctx.author.id)))
            contenders_file.close()


#changes to the voting phase--------------------------------------------------
@client.command(aliases=['change'])
@commands.has_role('Bartender')
async def separate(ctx):
    global fase_2
    if separated_vote == False and vote_start == False:
        await ctx.send("The voting session isn't separate.")

    elif separated_vote == False and fase_2 == False:
        await ctx.send("@everyone We are now changing to the voting phase.")
        fase_2 = False
    
    else:
        if vote_start == False:
            await ctx.send('There is no voting session in progress.')
        else:
            await ctx.send('We are already in the voting phase')


#returns the vote list---------------------------------------------------
@client.command()
async def votelist(ctx):
    embed = discord.Embed(title="The Votelist is:")
    for values in dict_for_voting:
        msg_to_add = "By " + str(dict_for_voting[values][1]) + " and has: " + str(dict_for_voting[values][2]) + " vote(s)"
        embed.add_field(name=str(dict_for_voting[values][0]), value=str(msg_to_add), inline=False)
    
    await ctx.send(embed=embed)


#casts a vote to the title called in by the user---------------------------------
@client.command()
async def vote(ctx, *, name):
    global dict_for_voting, voters
    if ctx.author.id not in voters:
        for value in dict_for_voting:
            if str(name).lower() == dict_for_voting[value][0].lower():
                await ctx.send("%s voted for: %s"%(ctx.author.name, dict_for_voting[value][0]))
                voters.update({ctx.author.id : [dict_for_voting[value][0], str(ctx.author.nick), str(dict_for_voting[value][3])]})
                dict_for_voting[value][2] += 1

                voters_file = open("voters.txt", "a")
                voters_file.write("%s, %s, " %(dict_for_voting[value][0], ctx.author.name))
                voters_file.close()

                print('%s voted for %s'%(ctx.author.id, name))
                print(dict_for_voting)
                print(voters)

    else:
        await ctx.send("you have already voted")


@client.command(aliases=['votename'])
async def vote_name(ctx, member:discord.Member):
    global dict_for_voting, voters
    if ctx.author.id not in voters:
        for value in dict_for_voting:
            if str(member.id) == dict_for_voting[value][3]:
                await ctx.send("%s voted for: %s"%(ctx.author.name, dict_for_voting[value][0]))
                voters.update({ctx.author.id : [dict_for_voting[value][0], str(ctx.author.nick), str(dict_for_voting[value][3])]})
                dict_for_voting[value][2] += 1

                voters_file = open("voters.txt", "a")
                voters_file.write("%s, %s, " %(dict_for_voting[value][0], ctx.author.name))
                voters_file.close()

                print('%s voted for %s'%(ctx.author.id, member.id))
                print(dict_for_voting)
                print(voters)

    else:
        await ctx.send("you have already voted")


#removes the vote casted by the user who called it---------------------------------------
@client.command(aliases=['remove'])
async def remove_vote(ctx):
    global voters, dict_for_voting
    if ctx.author.id in voters:
        for value in dict_for_voting:
            if voters[ctx.author.id][0] == dict_for_voting[value][0]:
                await ctx.send("%s your vote has been removed"%(ctx.author.name))
                dict_for_voting[value][2] -= 1
                del voters[ctx.author.id]
    
    else:
        await ctx.send("%s you haven't voted yet or you have already removed your vote"%(ctx.author.name))


#removes the contender called in by the author--------------------------------------------
@client.command(aliases=['removecontender', 'rc'])
@commands.has_role('Bartender')
async def remove_contender(ctx, member:discord.Member):
    global dict_for_voting, voters
    for value in dict_for_voting:
        for x in voters:
            if dict_for_voting[value][3] == str(member.id):
                if voters[x][0].lower() == dict_for_voting[value][0].lower():
                    del voters[x]
            await ctx.send('The contender %s by %s has been removed'%(dict_for_voting[value][0] ,dict_for_voting[value][1]))
            del dict_for_voting[value]
            print(dict_for_voting)
            print(voters)


#joins both contenders into a single contender called in by the author--------------------------------------------------
@client.command()
@commands.has_role('Bartender')
async def join(ctx, member:discord.Member, member2:discord.Member):
    global dict_for_voting, voters
    await ctx.send("Joining %s with %s."%(dict_for_voting[int(member.id)][0], dict_for_voting[int(member2.id)][0]))
    votes_to_add = 0
    votes_to_add += dict_for_voting[int(member2.id)][2]
    for value in voters:
        if voters[value][2] == dict_for_voting[int(member2.id)][3]:
            voters[value][2] = dict_for_voting[int(member.id)][3]
            voters[value][0] = dict_for_voting[int(member.id)][0]
    del dict_for_voting[int(member2.id)]
    dict_for_voting[int(member.id)][2] += votes_to_add
    print(dict_for_voting, voters)


# Decides the winner --------------------------------------------------------------------------------------------------------
@client.command(aliases=['finish'])
@commands.has_role('Bartender')
async def decide_winner(ctx):
    global winner
    highest_votes = 0
    if vote_start == False:
        if separated_vote == False and fase_2 == False:
            for value in dict_for_voting:
                if dict_for_voting[value][2] > highest_votes:
                    winner.clear()
                    winner.update({dict_for_voting[value][3] : [dict_for_voting[value][0], dict_for_voting[value][1], dict_for_voting[value][2], dict_for_voting[value][3]]})
                    highest_votes = int(dict_for_voting[value][2])

                elif dict_for_voting[value][2] == highest_votes:
                    winner.update({dict_for_voting[value][3] : [dict_for_voting[value][0], dict_for_voting[value][1], dict_for_voting[value][2], dict_for_voting[value][3]]})
                
            
            print(len(winner), winner)
            if len(winner) == 1:
                embed = discord.Embed(title="The winner is:")
                for value in winner:
                    winner_id = ''
                    winner_id += winner[value][3]
                    winner_2 = ('<@%s>'%(winner_id))
                    msg = "%s with %s votes, by:"%(winner[value][0], winner[value][2])
                    embed.add_field(name=msg, value=winner_2, inline=False)
                await ctx.send(embed=embed)
            
            elif len(winner) > 1:
                embed = discord.Embed(title="There is a tie between:")
                for value in winner:
                    winner_id = ''
                    winner_id += winner[value][3]
                    winner_2 = ('<@%s>'%(winner_id))
                    msg = "%s with %s votes, by:"%(winner[value][0], winner[value][2])
                    embed.add_field(name=msg, value=winner_2, inline=False)
                await ctx.send(embed=embed)

        elif separated_vote == False and fase_2 == False:
            await ctx.send("You are still on phase 1 please use b:separate to change phases")
        
        elif separated_vote == False:
            for value in dict_for_voting:
                if dict_for_voting[value][2] > highest_votes:
                    winner.clear()
                    winner.update({dict_for_voting[value][3] : [dict_for_voting[value][0], dict_for_voting[value][1], dict_for_voting[value][2], dict_for_voting[value][3]]})
                    highest_votes = int(dict_for_voting[value][2])

                elif dict_for_voting[value][2] == highest_votes:
                    winner.update({dict_for_voting[value][3] : [dict_for_voting[value][0], dict_for_voting[value][1], dict_for_voting[value][2], dict_for_voting[value][3]]})
                
            
            print(len(winner), winner)
            if len(winner) == 1:
                embed = discord.Embed(title="The winner is:")
                for value in winner:
                    winner_id = ''
                    winner_id += winner[value][3]
                    winner_2 = ('<@%s>'%(winner_id))
                    msg = "%s with %s votes, by:"%(winner[value][0], winner[value][2])
                    embed.add_field(name=msg, value=winner_2, inline=False)
                await ctx.send(embed=embed)
            
            elif len(winner) > 1:
                embed = discord.Embed(title="There is a tie between:")
                for value in winner:
                    winner_id = ''
                    winner_id += winner[value][3]
                    winner_2 = ('<@%s>'%(winner_id))
                    msg = "%s with %s votes, by:"%(winner[value][0], winner[value][2])
                    embed.add_field(name=msg, value=winner_2, inline=False)
                await ctx.send(embed=embed)
            
    else:
        await ctx.send("There is no voting session in progress")


@client.command()
async def help(ctx):
    embed = discord.Embed()
    embed.set_author(name="HELP")
    msg = [
        ("start", "Starts a voting session(NO PHASES)", False),
        ("start on", 'Starts a voting session with SEPARATE PHASES', False),
        ("stop", "Stops the ongoing voting session", False),
        ("add", "adds your contender for voting", False),
        ("change", "changes phases if the the ongoing voting session is separated", False),
        ("votelist", "Shows the current contenders and their votes", False),
        ("vote", "Votes using the exact title(NO CAPS NEEDED)", False),
        ("votename", "Votes for the user using his @", False),
        ("remove", "Removes your vote in case you voted for the wrong contender", False),
        ("rc, removecontender", "Removes the contender using his @", False),
        ("join", "Joins the contenders and their votes using their @'s", False),
        ("finish", "Stops the ongoing voting session and decides a winner", False),
    ]
    for name, value, inline in msg:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)


@client.command(aliases=['decision', 'decide', 'end'])
@commands.has_role('Bartender')
async def test(ctx, member=discord.Member):
    print(member)


client.run('NzI5MjI4NDk3NjY2NTcyMzYw.XwF49g.CgFbFirFkMFFqPkd4KcmW35G2eE')