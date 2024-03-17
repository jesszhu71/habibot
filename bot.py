from discord.ext import commands
import discord
import numpy as np
from collections import defaultdict


BOT_TOKEN = "REDACTED"
CHANNEL_ID = [1208122393932070982, 1208255739353628703, 1208256634825211904, 1208256708779057223, 1208256759660150824, \
              1208256816262422589, 1208256873183186944, 1208256931534471229]

GROCERY_CHANNELS = [1208122356925603880, 1208255714993242162, 1208256620795011133, 1208256682619183104, \
                    1208256746498564156, 1208256801485754368, 1208256858956111965, 1208256913951953008]

SOCIAL_CHANNELS = [1207928418893828156, 1207928628042670090, 1207956853821284402, 1207956874591477810, 1207956889917325352, 1207956903766917161, \
                   1207956923001999372, 1207956940236525638]

EVENT_CHANNELS = [1208124136334041108, 1208255692763430973, 1208256602235473940, 1208256658933809202, \
                  1208256729100460082, 1208256781055299625, 1208256837288468561, 1208256894360100874]

RENT_CHANNELS = [1215486191097348096, 1215486238371348500, 1215486528093028392, 1215486584200241222, 1215487467503751208, \
                 1215487937081376838, 1215488122985381898, 1215488878014627860
                 ]

# SPREADSHEETS = [ "https://docs.google.com/spreadsheets/d/1GRFyEkfTupWn4KcfSh8TzJDvX0o13wTG96GtSmKifkc/edit?usp=sharing",\
#                 "https://docs.google.com/spreadsheets/d/1d8EgrZ4b8kqDWRFFJDXq1aWstFix7r0_heEZiGeI0GM/edit?usp=sharing",\
#                 "https://docs.google.com/spreadsheets/d/12AxGo3Cm9xaDJD1JeYUUOGk9u6QZrPzeA9kJWqmat48/edit?usp=sharing", \
#                 "https://docs.google.com/spreadsheets/d/17x5Bl1RV6Mcn6_AG400AJb2B_V4jUkKgDL7cqDoOV88/edit?usp=sharing", \
#                 "https://docs.google.com/spreadsheets/d/1Mxo7gk8hK7rTGzf9lDvxxBsjUNHwD_ZB4ylq_8VOVwU/edit?usp=sharing", \
#                 "https://docs.google.com/spreadsheets/d/1yZXDy9h5dq1KiLbjbyg66glGgaTHscZ99ruo7Mno4u0/edit?usp=sharing", \
#                 "https://docs.google.com/spreadsheets/d/1YSx8C56hrqSM08mK7yfcm3CEDabsRtUMphP7MQSCJuo/edit?usp=sharing", \
#                 "https://docs.google.com/spreadsheets/d/1B91psm1bn8jDnmwOy-7VB-v0ehRgFTine6jawscmdOE/edit?usp=sharing" ]            




TEST_CHANNEL_ID = 1211872697630593024
grocery_list = {}
chore_status = {}

chore_dictionary = {}
chore_dictionary["\U0001F374"] = "clean the kitchen"
chore_dictionary["\U0001F6BD"] = "clean the bathroom"
chore_dictionary["\U0001F9F9"] = "sweeping/vacuuming the floor"
chore_dictionary["\U0001F5D1"] = "taking out the trash"



bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

points = defaultdict(int)


@bot.command()
async def rentTime(ctx):
    for channel_id in RENT_CHANNELS:
        channel = bot.get_channel(channel_id)
        rentMessage = await channel.send("Rent is due! This your reminder to pay rent by **03/16/2024**.\n\n" + 
                           "react here when you're done. ")
        await rentMessage.add_reaction("\U00002705")

@bot.command()
async def payBills(ctx):
    for channel_id in RENT_CHANNELS:
        channel = bot.get_channel(channel_id)
        members = channel.members
        mem = None
        for member in members:
            roles = [role.id for role in member.roles]
            if (1207932468670365696 not in roles and 1215431330213527603 not in roles):
                mem = member
                break
        if mem == None:
            mem = "_user here_"
        else:
            mem = mem.mention
        rentMessage = await channel.send("Groceries are $20 each today. This is your reminder to send payment to " + mem + ".\n\n" 
                                         + "react here when you're done. ")
        await rentMessage.add_reaction("\U00002705")

@bot.command()
async def clearAll(ctx):
    for channel_id in CHANNEL_ID:
        channel = bot.get_channel(channel_id)
        await channel.purge()
        await print_events(channel_id)
    for channel_id in GROCERY_CHANNELS:
        channel = bot.get_channel(channel_id)
        grocery_list[channel_id] = []
        await channel.purge()
        await channel.send("Manage your shared groceries here!\n\n" + 
                           "**!add ___ ** to add groceries \n" +
                            "**!removeItem ___ ** to remove item from list.\n" + 
                            "**!viewList ** to see the current list. \n" + 
                            "**!removeAll** to clear the current list.\n\n" + 
                            "i.e. **!add milk**, **!removeItem toilet paper**")
    for channel_id in SOCIAL_CHANNELS:
        channel = bot.get_channel(channel_id)
        await channel.purge()
        await channel.send("Chat with your housemates here! \n" + 
                           "This is your OG imessage chat that the imessage extension would be built off of.")
    for channel_id in EVENT_CHANNELS:
        channel = bot.get_channel(channel_id)
        await channel.purge()
        await channel.send("Schedule house things here!\n\n")
    for channel_id in RENT_CHANNELS:
        channel = bot.get_channel(channel_id)
        await channel.purge()
        await channel.send("This is where your bill reminders will appear.")
        


@bot.command()
async def getNewDay(ctx):
    for channel_id in CHANNEL_ID:
        
        await print_events(channel_id)


@bot.command()
async def remindChores(ctx):
    for channel_id in CHANNEL_ID:
        channel = bot.get_channel(channel_id)
        if (chore_status[channel_id] != 0):
            await channel.send("There are still " + str(chore_status[channel_id]) + "people that need to do your chores! \n"
                               "Please do them **ASAP**!")
        else:
            await channel.send("Thank you for doing your chores!")



@bot.command()
async def add(ctx, *item):
    if ctx.channel.id in grocery_list:
        s = ""
        for i in item:
            s = s + i + " "

        await ctx.send("**" + s + "** has been added to the grocery list")
        grocery_list[ctx.channel.id].append(s)


@bot.command()
async def removeAll(ctx):
    if ctx.channel.id in grocery_list:
        await ctx.send("Your grocery list has been cleared.")
        grocery_list[ctx.channel.id] = []



@bot.command()
async def viewList(ctx):
    if ctx.channel.id in grocery_list:
        if (len(grocery_list[ctx.channel.id]) == 0):
            await ctx.send("Your grocery list is empty")
        else:
            l = ""
            for item in grocery_list[ctx.channel.id]:
                l = l + "* " + item + "\n"
            await ctx.send("Here are all of your groceries\n" + l)



@bot.command()
async def removeItem(ctx, *item):
    if ctx.channel.id in grocery_list:
        s = ""
        for i in item:
            s = s + i + " "
        if (s in grocery_list[ctx.channel.id]):
            grocery_list[ctx.channel.id].remove(s)
            await ctx.send("**" + s + "** has been removed from the grocery list")
        else:
            await ctx.send(s + " is not in your grocery list\n")

    
@bot.event
async def on_ready():
    print("Chore bot is ready")
    for channel_id in CHANNEL_ID:
        for guild in bot.guilds:
            for member in guild.members:
                points[member] = 0






async def print_events(channel_id):

        channel = bot.get_channel(channel_id)
        choreMessage = await channel.send("Here are your chores for today: \n\n" +
                                        "\U0001F374 clean kitchen\n" +
                                        "\U0001F6BD clean bathroom \n" + 
                                        "\U0001F9F9 sweep/vacuum floor\n" + 
                                        "\U0001F5D1 take out the trash\n\n" + 
                                        "react here when you're finished!")
        await choreMessage.add_reaction("\U00002705")

        chore_status[channel_id] = 0

@bot.event
async def on_reaction_remove(reaction, user):
    message = reaction.message
    for channel_id in CHANNEL_ID:
        channel = bot.get_channel(channel_id)
        if message.channel.id == channel.id:
            if message.author == bot.user and user != bot.user:
                if reaction.emoji == "\U00002705":
                    points[user] = points[user] - 1
                    chore_status[channel_id] = chore_status[channel_id] - 1

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    for channel_id in CHANNEL_ID:
        channel = bot.get_channel(channel_id)
        if message.channel.id == channel.id:
            if message.author == bot.user and user != bot.user:
                if reaction.emoji == "\U00002705":
                    points[user] = points[user] + 1

                    chore_status[channel_id] = chore_status[channel_id] + 1


                    await handleChore(user, channel, points[user])   
                    await congrats(user, points, channel, channel_id)
               
                else:
                    await channel.send("not a valid emoji lmao")

async def congrats(user, points, channel, channel_id):
    channel_members = channel.members

    valid_members = 0
    for member in channel_members:
        roles = [role.id for role in member.roles]
        if (1207932468670365696 not in roles and 1215431330213527603 not in roles):
            valid_members = valid_members + 1
    
    if valid_members > chore_status[channel_id] or valid_members < chore_status[channel_id]:
        return
    await channel.send(str(valid_members))
    await channel.send("https://youtube.com/shorts/1tB7FpL4j3g?feature=share")
async def handleChore(user, channel, points):
    await channel.send("You now have **" + str(points) + "** point. \n")
    if (points == 1):
        await award_sticker(user, channel)

async def award_sticker(user, channel):
    await channel.send(user.mention + " You now have enough points to get an avatar sticker!")


bot.run(BOT_TOKEN)