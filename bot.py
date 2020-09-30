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
# vote_start = True
# separated_vote = True
# fase_2 = True

vote_start = False
separated_vote = False
fase_2 = False
continue_vote = False

# dict_for_voting = {274590558528471053: ['goh', 'ruflees', 1, '274590558528471053'], 745765600936067213: ['hxh', 'ruflees test', 2, '745765600936067213'], 108538100686274560: ['test', 'Brunao', 3, '108538100686274560']}
# voters = {745765600936067213: ['hxh', 'ruflees test', '745765600936067213'], 108538100686274560: ['test', 'Brunao', '108538100686274560']}
dict_for_voting = {}
voters = {}
tie_contenders = {}
tie_votes = {}
continue_voters = {}
winner = {}

vote_theme = []

yes_votes = 2
no_votes = 3

def update_winner():
    if yes_votes >= no_votes:
        winner.update({"yes": [yes_votes]})
        winner.update({"no": [no_votes]})
            
    else:
        winner.update({"no": [no_votes]})
        winner.update({"yes": [yes_votes]})

#starts a voting session-----------------------------------------------
@client.command()
@commands.has_role('Bartender')
async def start(ctx, arg="off", *, theme):
    global vote_start, separated_vote, vote_theme
    if vote_start == False:
        if arg.lower() == "on":
            separated_vote = True
        vote_start = True
        await ctx.send('A separated voting session has been started, please add your contenders.')
        
        embed = discord.Embed(
            colour = discord.Colour.blue()
        )

        embed.set_author(name="The theme is: %s"%(theme))

        await ctx.send(embed=embed)
        print("A voting session has been started")

        x = datetime.datetime.now()

        themes_file = open("data/themes/themes.txt", "a")
        themes_file.write("# %s/%s/%s: %s "%(x.strftime("%d"), x.strftime("%m"), x.strftime("%Y"), theme))
        themes_file.close()

        contenders_file = open("data/contenders/%s"%(theme), "a")
        voters_file = open("data/voters/%s"%(theme), "a")
        contenders_file.write(" # %s/%s/%s %s &: "%(x.strftime("%d"), x.strftime("%m"), x.strftime("%Y"), theme))
        voters_file.write(" # %s/%s/%s %s &: "%(x.strftime("%d"), x.strftime("%m"), x.strftime("%Y"), theme))
        contenders_file.close()
        voters_file.close()

        vote_theme.append(theme)
        print(vote_theme)


    elif vote_start == True:
        if separated_vote == True:
            await ctx.send('The separated voting session has already been started.')
        elif separated_vote == False:
            await ctx.send('The voting session has already been started.')


#stops the voting session------------------------------------------------------
@client.command()
@commands.has_role('Bartender')
async def stop(ctx):
    global vote_start,separated_vote, fase_2
    if vote_start == True:
        await ctx.send("The voting session has been stopped.")
        vote_start = False
        fase_2 = False
        separated_vote = False
        print("A voting session has been ended.")
    else:
        await ctx.send('There is no voting session in progress.')


#creates a contender called in by the author------------------------------------------
@client.command()
async def add(ctx, *, name):
    global dict_for_voting
    name_checker = [dict_for_voting[x][0].lower() for x in dict_for_voting]
    if vote_start == False:
        await ctx.send("There is no voting session in progress.")

    elif str(name.lower()) in name_checker:
        await ctx.send("A contender with the same name has already been added.")

    elif vote_start == True:
        if separated_vote == True and fase_2 == True:
            await ctx.send("%s the contender adding fase is already done."%ctx.author.mention)

        else:
            await ctx.send("%s added %s" %(ctx.author.name, name))
            if ctx.author.nick == None:
                dict_for_voting.update({ctx.author.id : [str(name), str(ctx.author.name), 0, str(ctx.author.id)]})
            else:
                dict_for_voting.update({ctx.author.id : [str(name), str(ctx.author.nick), 0, str(ctx.author.id)]})

            contenders_file = open("data/contenders/%s"%(vote_theme[0]), "a")
            contenders_file.write("%s, %s, %s, %s; " %(str(name), str(ctx.author.name), 0, str(ctx.author.id)))
            contenders_file.close()

            print(dict_for_voting)


#changes to the voting phase--------------------------------------------------
@client.command(aliases=['change'])
@commands.has_role('Bartender')
async def separate(ctx):
    global fase_2
    if separated_vote == False and vote_start == True:
        await ctx.send("The voting session isn't separate.")

    elif separated_vote == True and fase_2 == False:
        await ctx.send("@everyone We are now changing to the voting phase.")
        fase_2 = True
    
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
    
    print(dict_for_voting)
    print(voters)
    
    await ctx.send(embed=embed)


#casts a vote to the title called in by the user---------------------------------
@client.command()
async def vote(ctx, *, name):
    global dict_for_voting, voters
    if vote_start == True:
        if ctx.author.id not in voters:
            if separated_vote == True and fase_2 == False:
                await ctx.send("We aren't in the voting phase yet.")

            elif ctx.author.id in dict_for_voting:
                if str(name).lower() == dict_for_voting[ctx.author.id][0].lower():
                    await ctx.send("You cannot vote for yourself.")
            
            else:
                for value in dict_for_voting:
                    if str(name).lower() == dict_for_voting[value][0].lower():
                        print("test")
                        await ctx.send("%s voted for: %s"%(ctx.author.name, dict_for_voting[value][0]))
                        if ctx.author.nick == None:
                            voters.update({ctx.author.id : [dict_for_voting[value][0], str(ctx.author.name), str(dict_for_voting[value][3]), str(ctx.author.id)]})
                            dict_for_voting[value][2] += 1
                        else:
                            voters.update({ctx.author.id : [dict_for_voting[value][0], str(ctx.author.nick), str(dict_for_voting[value][3]), str(ctx.author.id)]})
                            dict_for_voting[value][2] += 1

                        voters_file = open("data/voters/%s"%(vote_theme[0]), "a")
                        voters_file.write("%s, %s, %s, %s, %s, 'ok'; " %(dict_for_voting[value][0], ctx.author.name, dict_for_voting[value][2], dict_for_voting[value][3], str(ctx.author.id)))
                        voters_file.close()

                        print('%s voted for %s'%(ctx.author.id, name))
                        print(dict_for_voting)
                        print(voters)

        else:
            await ctx.send("you have already voted")

    else:
        await ctx.send("There is no voting session in progress.")


@client.command(aliases=['votename'])
async def vote_name(ctx, member:discord.Member):
    global dict_for_voting, voters
    if vote_start == True:
        if ctx.author.id not in voters:
            if separated_vote == True and fase_2 == False:
                await ctx.send("We aren't in the voting phase yet.")
            
            elif int(member.id) in dict_for_voting:
                if str(ctx.author.id) == dict_for_voting[member.id][3]:
                    await ctx.send("You cannot vote for yourself.")

                else:
                    await ctx.send("%s voted for: %s"%(ctx.author.name, dict_for_voting[int(member.id)][0]))
                        
                    if ctx.author.nick == None:
                        voters.update({ctx.author.id : [dict_for_voting[int(member.id)][0], str(ctx.author.name), str(dict_for_voting[int(member.id)][3]), str(ctx.author.id)]})
                        dict_for_voting[int(member.id)][2] += 1
                    else:
                        voters.update({ctx.author.id : [dict_for_voting[int(member.id)][0], str(ctx.author.nick), str(dict_for_voting[int(member.id)][3]), str(ctx.author.id)]})
                        dict_for_voting[int(member.id)][2] += 1

                    voters_file = open("data/voters/%s"%(vote_theme[0]), "a")
                    voters_file.write("%s, %s, %s, %s, %s, 'ok'; " %(dict_for_voting[int(member.id)][0], ctx.author.name, dict_for_voting[int(member.id)][2], dict_for_voting[int(member.id)][3], str(ctx.author.id)))
                    voters_file.close()

                    print('%s voted for %s'%(ctx.author.id, member.id))
                    print(dict_for_voting)
                    print(voters)

        else:
            await ctx.send("you have already voted")

    else:
        await ctx.send("There is no voting session in progress.")


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

                voters_file = open("data/voters/%s"%(vote_theme[0]), "a")
                voters_file.write("%s, %s, %s, %s, %s, 'removed'; " %(dict_for_voting[value][0], dict_for_voting[value][1], dict_for_voting[value][2], dict_for_voting[value][3], ctx.author.id))
                voters_file.close()
    
    else:
        await ctx.send("%s you haven't voted yet or you have already removed your vote"%(ctx.author.name))


#removes the contender called in by the author--------------------------------------------
@client.command(aliases=['removecontender', 'rc'])
@commands.has_role('Bartender')
async def remove_contender(ctx, member:discord.Member):
    global voters
    print(member.id)
    delete_id = []
    for value in voters:
        if voters[value][2] == dict_for_voting[member.id][3]:
            delete_id.append(voters[value][3])

    print(delete_id)

    for value in delete_id:
        del voters[int(value)]

    print("test")

    contenders_file = open("data/contenders/%s"%(vote_theme[0]), "a")
    contenders_file.write("%s, %s, %s, %s, 'removed'; " %(str(dict_for_voting[member.id][0]), str(dict_for_voting[member.id][1]), 0, str(dict_for_voting[member.id][3])))
    contenders_file.close()

    await ctx.send('The contender %s by %s has been removed'%(dict_for_voting[member.id][0] ,dict_for_voting[member.id][1]))

    del dict_for_voting[member.id]

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

    contenders_file = open("data/contenders/%s"%(vote_theme[0]), "a")
    contenders_file.write("%s, %s, %s, %s, 'removed'; " %(str(dict_for_voting[member2.id][0]), str(dict_for_voting[member2.id][1]), 0, str(dict_for_voting[member2.id][3])))
    contenders_file.close()

    voters_file = open("data//%s"%(vote_theme[0]), "a")
    voters_file.write("%s, %s, %s, %s; " %(dict_for_voting[int(member.id)][0], dict_for_voting[int(member.id)][1], dict_for_voting[int(member.id)][2], dict_for_voting[int(member.id)][3]))
    voters_file.close()


# Decides the winner --------------------------------------------------------------------------------------------------------
@client.command(aliases=['finish'])
@commands.has_role('Bartender')
async def decide_winner(ctx):
    global vote_start, separated_vote, fase_2
    if vote_start == True:
        if separated_vote == True and fase_2 == False:
            await ctx.send("You are still on adding phase please use b:separate to change phases")
        
        else:
            dict_for_voting_sorted = sorted(dict_for_voting.items(), key=lambda x: x[1], reverse=True)
            
            print(dict_for_voting_sorted)
            await ctx.send("test")

            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name="These are the top #3")
            msg = [
                ("#1 %s"%(dict_for_voting_sorted[0][1][0]), "by <@%s> with %s votes"%(dict_for_voting_sorted[0][1][3], dict_for_voting_sorted[0][1][2]), False),
                ("#2 %s"%(dict_for_voting_sorted[1][1][0]), "by <@%s> with %s votes"%(dict_for_voting_sorted[1][1][3], dict_for_voting_sorted[1][1][2]), False),
                ("#3 %s"%(dict_for_voting_sorted[2][1][0]), "by <@%s> with %s votes"%(dict_for_voting_sorted[2][1][3], dict_for_voting_sorted[2][1][2]), False),
            ]
            for name, value, inline in msg:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

            vote_start = False
            separated_vote = False
            fase_2 = False
                 
            
    else:
        await ctx.send("There is no voting session in progress")


# Clears dict_for_voting -------------------------------------------------------------------------------------------------------------------
@client.command()
@commands.has_role('Bartender')
async def clear(ctx):
    global dict_for_voting, vote_theme
    dict_for_voting.clear()
    voters.clear()
    vote_theme.clear()

    print(vote_theme)
    await ctx.send("The voting list has been cleared.")


@client.command(aliases=['continue'])
@commands.has_role('Bartender')
async def _continue(ctx, arg):
    global continue_vote, yes_votes, no_votes, winner, continue_voters
    if arg.lower() == "start":
        if continue_vote == True:
            await ctx.send("A voting session to continue has already been started.")

        elif continue_vote == False:
            await ctx.send("A voting session to continue has been started. Use b:yes or b:no to vote.")
            continue_vote = True

    elif arg.lower() == "stop":
        if continue_vote == False:
            await ctx.send("No voting session to continue has been started.")

        elif continue_vote == True:
            continue_vote = False

            update_winner()

            winner_sorted = sorted(winner.items(), key=lambda x: x[1], reverse=True)

            print(winner_sorted)

            await ctx.send("A voting session to continue has been ended.")


            embed = discord.Embed(
                colour = discord.Colour.red()
            )
            embed.set_author(name="Continue voting results:")

            msg = [
                ("#1 %s"%(winner_sorted[0][0]), "with: %s votes"%(winner_sorted[0][1][0]), False),
                ("#2 %s"%(winner_sorted[1][0]), "with: %s votes"%(winner_sorted[1][1][0]), False),
            ]

            for name, value, inline in msg:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

            winner.clear()
            winner_sorted.clear()
            continue_voters.clear()

            yes_votes = 0
            no_votes = 0

            print(winner, winner_sorted, continue_voters, yes_votes, no_votes)


@client.command()
async def yes(ctx):
    global continue_voters, continue_vote, yes_votes
    if continue_vote == True:
        if ctx.author.id not in continue_voters:
            if ctx.author.nick == None:
                continue_voters.update({ctx.author.id : ["yes", str(ctx.author.name), str(ctx.author.id)]})
                yes_votes += 1
            else:
                continue_voters.update({ctx.author.id : ["yes", str(ctx.author.nick), str(ctx.author.id)]})
                yes_votes += 1

            print(yes_votes, continue_voters)
            embed_1 = discord.Embed(
                colour = discord.Colour.blue()
            )

            embed_1.set_author(name="%s you voted YES"%(continue_voters[ctx.author.id][1]))
            await ctx.send(embed=embed_1)

            update_winner()

            winner_sorted = sorted(winner.items(), key=lambda x: x[1], reverse=True)

            embed = discord.Embed(
                colour = discord.Colour.red()
            )
            embed.set_author(name="Continue voting results:")

            msg = [
                ("#1 %s"%(winner_sorted[0][0]), "with: %s votes"%(winner_sorted[0][1][0]), False),
                ("#2 %s"%(winner_sorted[1][0]), "with: %s votes"%(winner_sorted[1][1][0]), False),
            ]

            for name, value, inline in msg:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

        else:
            await ctx.send("You have already voted.")

    else:
        await ctx.send("There is no voting session to continue in progress.")


@client.command()
async def no(ctx):
    global continue_voters, continue_vote, no_votes
    if continue_vote == True:
        if ctx.author.id not in continue_voters:
            if ctx.author.nick == None:
                continue_voters.update({ctx.author.id : ["no", str(ctx.author.name), str(ctx.author.id)]})
                no_votes += 1
            else:
                continue_voters.update({ctx.author.id : ["no", str(ctx.author.nick), str(ctx.author.id)]})
                no_votes += 1

            print(yes_votes, continue_voters)
            embed_1 = discord.Embed(
                colour = discord.Colour.blue()
            )

            embed_1.set_author(name="%s you voted NO"%(continue_voters[ctx.author.id][1]))
            await ctx.send(embed=embed_1)

            update_winner()

            winner_sorted = sorted(winner.items(), key=lambda x: x[1], reverse=True)

            embed = discord.Embed(
                colour = discord.Colour.red()
            )
            embed.set_author(name="Continue voting results:")

            msg = [
                ("#1 %s"%(winner_sorted[0][0]), "with: %s votes"%(winner_sorted[0][1][0]), False),
                ("#2 %s"%(winner_sorted[1][0]), "with: %s votes"%(winner_sorted[1][1][0]), False),
            ]

            for name, value, inline in msg:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

        else:
            await ctx.send("You have already voted.")

    else:
        await ctx.send("There is no voting session to continue in progress.")


@client.command(aliases=['removecontinue', 'delcontinue'])
@commands.has_role('Bartender')
async def remove_continue(ctx):
    global continue_voters, yes_votes, no_votes
    if continue_vote == True:
        if ctx.author.id in continue_voters:
            print(continue_voters)

            if continue_voters[ctx.author.id][0] == "yes":
                yes_votes -= 1
            elif continue_voters[ctx.author.id][0] == "no":
                no_votes -= 1
            
            del continue_voters[ctx.author.id]
            
            print(continue_voters)

            await ctx.send("Your continue vote has been removed")

            update_winner()

            winner_sorted = sorted(winner.items(), key=lambda x: x[1], reverse=True)

            embed = discord.Embed(
                colour = discord.Colour.red()
            )
            embed.set_author(name="Continue voting results:")

            msg = [
                ("#1 %s"%(winner_sorted[0][0]), "with: %s votes"%(winner_sorted[0][1][0]), False),
                ("#2 %s"%(winner_sorted[1][0]), "with: %s votes"%(winner_sorted[1][1][0]), False),
            ]

            for name, value, inline in msg:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)
        
        else:
            await ctx.send("You haven't voted yet.")
    else:
        await ctx.send("There is no voting session to continue in progress.")


@client.command()
@commands.has_role('Bartender')
async def recover(ctx):
    pass


# prints all the commands and their functions ----------------------------------------------------------------------------------
@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.red()
    )
    embed.set_author(name="HELP")
    msg = [
        ("-SÓ PARA MODS", "-------------------------", False),
        ("start off (theme)", "Começa uma votação (SEM FASES)", False),
        ("start on (theme)", 'Começa uma votação (COM FASES)', False),
        ("stop", "Para a votação em andamento", False),
        ("rc, removecontender", "Remove o competidor", False),
        ("join", "Junta os competidores e seus votos usando a @ de quem os cadastrou", False),
        ("finish", "Termina a votação em andamento e define um ganhador", False),
        ("clear", "Limpa a votelist", False),
        ("continue start", "Começa uma votação para continuar", False),
        ("continue stop", "Termina a votação para continuar e mostra os resultados(IRÁ LIMPAR OS DADOS APÓS ENCERRAR!)", False),
        ("-CLIENTES", "-------------------------", False),
        ("add", "Adiciona o seu competidor para votação", False),
        ("change", "Troca a fase da votação", False),
        ("votelist", "Mostra os competidores e sua contagem de votos", False),
        ("vote", "Vota usando o nome do competidor(NÃO PRECISA DE CAPS)", False),
        ("votename", "Vota usando @ de quem o cadastrou", False),
        ("remove", "Remove o seu voto caso votou para o competidor errado", False),
        ("yes", "Vota SIM para continuar", False),
        ("no", "Vote NÃO para continuar", False),
        ("removecontinue, delcontinue", "Remove o seu voto para continuar caso votou errado", False),
    ]
    for name, value, inline in msg:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)


@client.command()
@commands.has_role('Bartender')
async def test(ctx, member:discord.Member):
    member_id = ("<@%s>"%(member.id))
    await ctx.send(member_id)
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name=member_id)
    await ctx.send(embed=embed)


client.run('NzI5MjI4NDk3NjY2NTcyMzYw.XwF49g.CgFbFirFkMFFqPkd4KcmW35G2eE')