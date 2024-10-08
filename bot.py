'''
# bot.py
# bot server back end and front end for interaction with
# server.
# date: 6/23/21
# author: dnglokpor
'''

# imports
import discord, os, sys                   # environment
import time as tm                         # timer
from dotenv import load_dotenv            # sensitive data cache
import logging                            # logging util
from discord.ext import commands as com   # discord lib
import discord.ext.commands.errors as err # errors
from discord.ext.commands import DefaultHelpCommand # help object
import random as rnd                      # randomizer
from math import ceil
try:
   import cPickle as pickle               # pickle
except ModuleNotFoundError:
   import pickle

# add game world package to path so that internal imports work
sys.path.insert(0, os.getcwd() + "/world")
# add pictures generation package to path
sys.path.insert(0, os.getcwd())

# game world package imports
from idleUser import IdleUser, save, load, USER_PICS_PATH,\
   USER_RECORDS_PATH, USER_TEMPS_PATH, HERO_SAVES_PATH
import picsGen as pg
from world.helpers import timeString
import collectibles as c
from world.collectibles import Gear, Weapon, Armor, Accessory
import world.itemLib as il
from world.classes import Fighter, Ranger, Elementalist
from world.confrontation import Party
from world.dungeon import DUNGEON

# bot config
load_dotenv()        # loads .env data
# attach bot commands prefixes
PREFIXES = ['>', '/', ';' ]

# override bot help command
class CustomHelpCommand(DefaultHelpCommand):
   '''Subclass of HelpCommand that allows me to override the 
   response commands.'''
   def __init__(self):
      '''build base class.'''
      super().__init__()
   
   # overrides
   async def send_bot_help(self, mapping):
      '''send out a help message for the whole bot'''
      ctx = self.context
      msg = buildResponse(ctx) # salutation
      msg += " Welcome to the IdleFantasyBot support.\n\n"
      msg += "This bot allows you to run an idle exploration of the **Idle Dungeon** "
      msg += "the most dangerous dungeon in the whole of the lands. Each floor "
      msg += "has its own environment where numerous resources are available "
      msg += "but where devious monsters wreck havoc as well. Will you be able "
      msg += "to conquer it all?\n\n"
      msg += "**Quick Start Guide:**\n"
      msg += "Use the `;guild` command to register yourself as a player.\n"
      msg += "Use the \n`;hero <class name>`\ncommand to add a hero avatar to your account "
      msg += "out of the existing classes: **Fighter**, **Ranger** and **Elementalist**.\n"
      msg += "You can see an overview of your account and hero using the `;profile` "
      msg += "command and using `;bag` will reveal your inventory and money.\n"
      msg += "Finally, to explore a floor, you will need to use the\n"
      msg += "`;explore <floor number>`\ncommand. but it would be wise "
      msg += "to first gather information on the floor by using\n"
      msg += "`;scout <floor number>`.\nLater, you can add other players "
      msg += "to your friendbook and call upon to go on an adventure with you:\n"
      msg += "`;explore <floor number> [friend list]`\nCheck out `myplayerid`, "
      msg += "`befriend` and `friendbook` commands for more infor on friends."
      msg += "\n\n**Here are all the available commands:**\n"
      commands = bot.commands
      for i, command in enumerate(commands):
         msg += command.name
         if i < len(commands) - 1:
            msg += ", "
         else:
            msg += '.\n'
      msg += "\nUse `;help <command>` to get specific help on each command.\n\n"
      msg += "We hope you enjoy your time using IdleFantasyBot."
      await ctx.message.channel.send(msg)

# instantiate bot instance

intents = discord.Intents.default()
intents.message_content = True

bot = com.Bot(command_prefix = PREFIXES,
      help_command = CustomHelpCommand(),
      intents = intents
   )
# logging
REPORT_DIR = "logs" # path to log file
REPORT_FILE = "eventLog.txt" # log file
# shop stocks
ALWAYS = [
   il.s_Arrow, il.s_Axe, il.s_Pickaxe, il.s_WalkingStick, 
   il.s_Apprensteel, il.s_HuntingBow, il.s_ElementalWand,
   il.s_LeatherArmor, il.s_SilkRobe, il.s_SurvivalVest
]   
# helpers
def senderInfo(ctx: com.Context):
   '''uses the context to return the channel and mention
   of author of the message received.'''
   return (ctx.message.channel, ctx.message.author.mention)

def eReport(report):
   '''uses the logging module to quickly save the report 
   in a file''' 
   # dir doesn't exist
   if not os.path.isdir(REPORT_DIR):
      os.mkdir(REPORT_DIR) # create the folder   
   
   # config logger
   fm = 'a'       # appending by default
   if not os.path.exists(REPORT_DIR + '/'+ REPORT_FILE): # file doesn't exist
      fm = "w+"   # then create and append
   logging.basicConfig(filename = REPORT_DIR + '/'+ REPORT_FILE,
      format = "%(asctime)s %(process)d %(message)s",
      datefmt = "%d-%b-%y %H:%M:%S", filemode = fm
   )
                        
   # making log object
   logger = logging.getLogger()
   logger.setLevel(logging.DEBUG)
   logger.propagate = False
   
   # log the report
   logger.info(report)

def logError(eData):
   '''logs an error that occured at runtime. "eData" must
   be the tuple generated by sys.exc_info().'''
   eData
   eString = eData[0] + '\n' + eData[1]
   print(eString)    # console print it
   eReport(eString)  # report log it 
   # print trace to report file
   print(eData[2], file = REPORT_DIR + '/'+ REPORT_FILE)

# back end
# finds if a user is a registered user
def isRegistered(id: int) -> bool:
   '''checks if the passed id is associated with an
   existing user record file.'''
   userfile = USER_RECORDS_PATH + '/' + str(id) + ".usr"
   return os.path.isfile(userfile)

# terminates if not (registered w/ hero)
async def isRegisteredWithHero(ctx):
   '''checks for registration and hero. if either is missing
   an error message is sent to the command author.'''
   id = ctx.message.author.id
   username = ctx.message.author.name
   channel, mention = senderInfo(ctx)
   valid = True
   if not isRegistered(id):
      valid = False
      await waitThenSend(ctx, nRegMSG.format(mention))
   else: # they are registered so we check for hero
      with open(USER_RECORDS_PATH + str(id) + ".usr", 'r') as record:
         valid = ((((record.read()).split('\n'))[3]).split())[1]
      valid = valid == "True"
      if not valid:
         await waitThenSend(ctx, nHeroMSG.format(mention))
   return valid

# transfer sensitive data
def recoverData(u: IdleUser):
   '''transfer some data from the current user file to 
   the passed user object.'''
   current = load(u.getID())
   u.open = current.open # coop status
   u.friendbook = current.friendbook # friendbook
   u.getHero().wallet = current.getHero().getWallet() # wallet

# rescue algorithm
async def rescueFallen(key: int, floor: int) -> list:
   '''rescue a fallen adventurer/party if they were defeated
   on the floor the player is exploring. return a list
   representing things recovered from the fallen as reward.
   if no reward was found, return '''
   temp = USER_TEMPS_PATH + str(key) + ".resq"
   rewards = None
   if os.path.isfile(temp): # fallen party exist
      with open(temp, "rb") as file:
         data = pickle.load(file) # recover data
         if data["floor"] == floor:
            rewards = list()
            for fallen in data["users"]:
               # possible reward from fallen
               bag = fallen.getHero().getBag()
               if not bag.isEmpty():
                  stack = rnd.choice(list(bag.contents.values()))
                  rewards.append((stack[0], len(stack)))
               # free user
               fUser = load(fallen.getID())
               fUser.inCity = True
               fUser.setKey(0) # reset exploration key
               recoverData(fUser)
               save(fUser)
               # tell fallen user he was rescued
               dm = await getDM(fUser)
               await dm.send("`you have been rescued. please be careful "
                  "next time.`")
      os.remove(temp) # erase the file
   return rewards

@bot.event
async def on_ready():
   readyMSG = "We have logged in as {}\n".format(bot.user)
   print(readyMSG)
   # get all guilds
   readyMSG += "online in servers:\n"
   for g in bot.guilds:
      readyMSG += "{}\t".format(g)
   eReport(readyMSG)

# command errors override
@bot.event
async def on_command_error(ctx: com.Context, exception):
   '''deal with errors at bot commands execution for
   a smooth runtime.'''
   channel, mention = senderInfo(ctx)
   command = ctx.command
   if type(exception) == err.CommandNotFound:
      await waitThenSend(ctx,
         "{}, that command doesn't exist. Use `help` to see"
         " all available commands.".format(mention)
      )
   elif type(exception) == err.MissingRequiredArgument:
      msg = "{} you forgot to specify ".format(mention)
      if command.name == "hero":
         msg += "the hero class you want to use.\n"
         msg += "`eg.: ;hero Fighter`"
      elif  command.name == "scout":
         msg += "the floor which info you seek.\n"
         msg += "`eg.: ;scout 1`"
      elif  command.name == "rescue":
         msg += "the key of the fallen party. they should have sent "
         msg += "you one.\n"
         msg += "`eg.: ;rescue 1234567890`"
      elif  command.name == "lookup":
         msg += "the name of the item you are attempting to lookup."
         msg += "eg.: `;lookup arrow` or `;lookup \"iron ore\"`."
      elif  command.name == "buy":
         msg += "the name of the item you are attempting to buy."
         msg += "eg.: `;buy arrow` or `;buy \"iron ore\"`."
      elif  command.name == "sell":
         msg += "the name of the item you are attempting to sell."
         msg += "eg.: `;buy arrow` or `;buy \"iron ore\"`."
      elif  command.name == "equip":
         msg += "the name of the item you are attempting to equip."
         msg += "eg.: `;equip sword` or `;equip \"stone shield\"`."
      else:
         msg += "a required argument. if you're typing a composite "
         msg += "name, you might have forgot the quotes around it?\n"
         msg += "use `;help {}".format(command.name)
         msg += "` to see the correct use."
      await waitThenSend(ctx, msg)
   elif type(exception) == err.BadArgument:
      msg = "this command was wrongly used. use `;help {}".format(command.name)
      msg += "` to see the correct use."
      await waitThenSend(ctx, msg)
   else: # unknow error
      server = ctx.guild
      triggerUser = ctx.me
      triggerCom = ctx.command
      eReport("error on {} by {} on server {}".format(
         triggerCom, triggerUser, server)) # log trigger info
      eReport(str(type(exception.__cause__)))
      eReport(str(exception.__cause__))
      await waitThenSend(ctx, 
         "Something went wrong. Sorry, try something else.", 2)

# front end
def buildResponse(ctx: com.Context) -> str:
   '''creates a reply to a hello command by mentionning
   the sender and in a randomly selected formula return
   it to the caller.'''
   hellos = ["Hi", "Oh hello there", "Hiya", "What's up",
      "What's cooking", "Ohayo"
   ]
   mention = ctx.message.author.mention
   return " ".join([rnd.choice(hellos), mention])

# delayed response
async def waitThenSend(ctx: com.Context, message: str,
   wait = 1):
   '''sends the passed "message" to the specified channel
   after waiting "wait" seconds.'''
   tm.sleep(wait)
   await ctx.send(message)

# recover user client
async def getDiscordUser(id: int):
   '''uses the id of a discord user to recover the
   discord.Client.User object associated with it and return
   it.'''
   uObject = await bot.fetch_user(id)
   return uObject

# find dm channel
async def getDM(user: IdleUser):
   '''retrieve a dm channel from a IdleUser user account.'''
   uObject = await getDiscordUser(user.getID())
   dm_channel = uObject.dm_channel
   if dm_channel == None:
      dm_channel = await uObject.create_dm()
   return dm_channel

@bot.command(name = "hello",
   help = "Says hello to the username, using a randomly choosed formula.")
async def hello(ctx):
   '''Says Hi to the username.'''
   channel, mention = senderInfo(ctx)
   await waitThenSend(ctx, buildResponse(ctx))


# premade messages
nRegMSG = "You are not registered {}. "\
   "Use the `guild` command to register first."
nHeroMSG = "You don't have a hero {}. use the `hero` "\
   "command to register a hero to your account."
tips = [
   "Use the `profile` command to get your account status.",
   "Use the `bag` command to display the contents of your "
   "bag.",
   "Use the `explore` command to send your hero on a dungeon "
   "exploration. during exploration, you will be considered "
   "**not in the city**.",
   "Your hero's health **heals by itself** as time goes by.",
   "If you die during an exploration, your hero's party will"
   " be stuck on that floor until someone saves them. You "
   "need to share the key you receive in the message with "
   "other players.",
]

# register player
@bot.command(name = "guild", help = "register the user as a "
   "potential player of the game by recording their id and "
   "username. then display the instructions for them to pick "
   "their hero. also record the user profile picture.")
async def guild(ctx):
   '''record user if they are not recorded yet. give instructions
   on how to select a hero.'''
   id = ctx.message.author.id
   username = ctx.message.author.name
   channel, mention = senderInfo(ctx)
   if isRegistered(id): # user already exists
      msg = "{} you are already registered. ".format(mention)
      msg += "Use the `help` command to see what commands"\
      " are available to you."
      await waitThenSend(ctx, msg)
   else: # new user
      # register them
      newUser = IdleUser(id, username)
      # record user avatar as picture
      author = ctx.message.author
      avatarAsset = author.avatar.replace(format = "png")
      userpic = USER_PICS_PATH + str(id) + '.png'
      await avatarAsset.save(userpic)
      newUser.setPic(userpic)
      # save to permanent record
      save(newUser)
      # reply to them
      msg = "Welcome to the Idle Guild {}. We are so happy to "\
      "have you with us. Without further ado, let's register "\
      "you as an adventurer. "\
      "We do need to know what class of adventurer you are. "\
      "There are three possible classes: **Fighter**, "\
      "**Ranger** and **Elementalist**. Use the `hero` "\
      "command to specify your class.\n"
      "`eg: >hero Fighter`"
      await waitThenSend(ctx, msg.format(mention))

# add a hero to player account
@bot.command(name = "hero", help = "allows a user to add a "
   "hero to their account. heroes are necessary to be able "
   "to explore the dungeon, or interact with city facilities.\n"
   "possible choices: **Fighter**, **Ranger**, **Elementalist**.\n"
   "`eg: ;hero Fighter`.")
async def hero(ctx, className: str):
   '''loads a registered user's profile and if they don't 
   yet have a hero.'''
   id = ctx.message.author.id
   username = ctx.message.author.name
   channel, mention = senderInfo(ctx)
   if not isRegistered(id):
      msg = nRegMSG.format(mention)
   elif load(id).hasHero():
      msg = "You already have a hero {}. ".format(mention)
      msg += "Everyone only gets one. Don't be greedy."
   else: # registered user w/ no hero
      user = load(id)
      msg = "Congratulations {}. ".format(mention)
      token = str()
      done = className.lower() in ["fighter", "ranger", "elementalist"]
      if className.lower() == "fighter":
         user.setHero(Fighter(username))
         msg += "You are now a Fighter"
         token = ":crossed_swords:"
      elif className.lower() == "ranger":
         user.setHero(Ranger(username))
         msg += "You are now a Ranger"
         token = ":bow_and_arrow:"
      elif className.lower() == "elementalist":
         user.setHero(Elementalist(username))
         msg += "You are now an Elementalist"
         token = ":magic_wand:"
      else:
         await waitThenSend(ctx, 
            "**{}** is not a know hero class.".format(className))
      if done:
         msg = token + msg + token + '\n'
         for tip in tips:
            msg += tip + '\n' #+ tips[1] + '\n' + tips[2] + '\n'
         save(user)
         await waitThenSend(ctx, msg)

# display player account info
@bot.command(name = "profile", help = "show the player's profile "
   "status page.")
async def profile(ctx):
   '''sends a profile status page to the author of the message
   if they are registered players.'''
   mention = ctx.message.author.mention
   if (isRegistered(ctx.message.author.id)):
      user = load(ctx.message.author.id)
      profile = discord.File(pg.genProfile(user))
      await ctx.send("here is your profile {}:".format(mention), 
         file = profile)
   else:
      await ctx.send(nRegMSG.format(mention)) 

# display avatar inventory
@bot.command(name = "bag", help = "get an image describing your "
   "main inventory contents. your main inventory is the bag of "
   "your hero.\neg.: ;bag")
async def bag(ctx):
   if (await isRegisteredWithHero(ctx)): # terminates in case of no hero
      user = load(ctx.message.author.id)
      bag = discord.File(pg.genBag(user))
      mention = ctx.message.author.mention
      await ctx.send("here's what you own {}:".format(mention), 
         file = bag)
         
# shows learnable skills
@bot.command(name = "learnable", help = "shows you the all the "
   "skills that can be learned by your hero.")
async def learnable(ctx):
   if (await isRegisteredWithHero(ctx)): # terminates in case of no hero
      user = load(ctx.message.author.id)
      mastery = user.getHero().getMastery().__str__(False)
      await waitThenSend(ctx, mastery)

# shows learned skills
@bot.command(name = "learned", help = "shows you the all the "
   "skills your hero has learned.")
async def learned(ctx):
   if (await isRegisteredWithHero(ctx)): # terminates in case of no hero
      user = load(ctx.message.author.id)
      mastered = user.getHero().getMastery().getUnlocked(
         user.getHero().getLevel().getCurrent())
      msg = "Learned skills:\n"
      for skill in mastered:
         msg += '`' + skill.__str__() + '`'
         msg += "\n------------------------------\n"
      await waitThenSend(ctx, msg)

# show floor information
@bot.command(name = "scout", help = "display information on "
   "the specified floor. if you have never completed the exploration "
   "of said floor, only its size and danger levels will be available."
   " explore it to unlock more info about the resources and hostiles."
   "\neg: `>scout 1`")
async def scout(ctx, floor: int):
   if isRegistered(ctx.message.author.id):
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      if floor < 1:
         await waitThenSend(ctx, "Invalid floor!!!")
      elif not DUNGEON.__contains__(floor):
         resp = mention
         resp += " , that floor isn't available yet."
         await waitThenSend(ctx, resp)
      else: # we are good
         info = mention
         info += " here is the intelligence on floor {}:\n".format(floor)
         if floor <= user.getTopFloor(): # already explored
            info += DUNGEON[floor].__str__(True)
         else: # never explored
            info += DUNGEON[floor].__str__()
            info += "\n*explore it to unlock more info.*"
         await waitThenSend(ctx, info)
   else:
      await waitThenSend(ctx, nRegMSG)

# set up user for exploration
def readyUser(user: IdleUser, start: int):
   '''set the appropriate user flags and the key needed
   for the user to be exploration ready.'''
   user.inCity = False
   user.setKey(start)
   save(user)

# explore dungeon
@bot.command(name = "explore", help = "explore the specified "
   "floor of the dungeon. you can specify up to **3** other players "
   "to explore with. just specify their ID in your Friendbook. "
   "separeted by a comma (no spaces allowed). they must be in "
   "your Friendbook to be allowed in your party. exploring a block "
   "takes `2min` so exploring a floor takes `2min * size of floor`."
   "\neg.: `;explore 1` or `;explore 1 reac1,bail2,susa3`")
async def explore(ctx, f: int, allies: str=None):
   # in case of empty allies
   if allies == None:
      allies = "" # empty string
   do = False
   start = 0
   if (await isRegisteredWithHero(ctx)): # terminates in case of no hero
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      if f < 1:
         await waitThenSend(ctx, "Invalid floor!!!")
      elif not DUNGEON.__contains__(f):
         resp = mention
         resp += " , that floor isn't available yet."
         await waitThenSend(ctx, resp)
      elif f > user.getTopFloor() + 1:
         resp = mention
         resp += ", you can't go to that floor yet. you still"
         resp += " need to explore floor {}".format(
            user.getTopFloor() + 1)
         await waitThenSend(ctx, resp)
      else: # floor is in reach
         if not (user.isInCity()):
            resp = mention
            resp += ", you have to be `in town` to go on "
            resp += "exploration."
            await waitThenSend(ctx, resp)
         else: # free and ready to explore
            do = True
            start = int(tm.time()) # timer
            # update user disponibility
            readyUser(user, start)
   if do: # exploration setup block
      going = [user,]
      # add coop heroes
      if allies != "":
         allies = allies.split(',')
         if len(allies) > 4:
            allies = allies[:3] # only keep three
            await waitThenSend(ctx,
               "only 3 others can accompany you {}.".format(mention))
         for a in allies:
            friend = user.getFriendBook().getFriend(a)
            if friend != None:
               friend = load(friend[0])
               if friend.hasHero() and friend.canCoop():
                  going.append(friend)
                  readyUser(friend, start)
                  fMSG = "**{}** invited to explore floor {}.".format(
                     user.getUname(), f)
                  fMSG += " use `;report` to check on the status the exploration."
                  dm = await getDM(friend)
                  await dm.send(fMSG)
               else:
                  await waitThenSend(ctx,
                     "{} is not available for coop.".format(
                        friend.getUname()))
            else: # no user of that name in phonebook
               msg = "you don't have a friendbook entry with **FID** "
               msg += "{}. check your FriendBook for correct ".format(a)
               msg += "**FIDs** (it's the third entry on each line)."
               await waitThenSend(ctx, msg)
      setupData = {
         "startTime": start,
         "floor": f,
         "users": going
      }
      with open(USER_TEMPS_PATH + str(start) + ".wait", "wb") as setupFile:
         pickle.dump(setupData, setupFile, pickle.HIGHEST_PROTOCOL)
      # the rest will be ran by the bg_explorer.py process
      # announce that the party has left
      msg = ""
      for u in going:
         msg += u.getUname()
         if u != going[-1]:
            msg += ", "
      msg += " go on an exploration of the {} floor ".format(f)
      msg += "for `{}`.".format(timeString(DUNGEON[f].getSize() * 120))
      msg += " use `;report` to check on the status the exploration."
      await waitThenSend(ctx, msg)

# report command
@bot.command(name = "report", help = "report on the exploration that "
   "the player went on. if exploration isn't over, says how much "
   "time remains.")
async def report(ctx):
   '''report on exploration status.'''
   if (await isRegisteredWithHero(ctx)):
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      if user.isInCity():
         await waitThenSend(ctx,
            "you didn't go on any exploration {}.".format(mention))
      else: # was on an exploration
         # try loading temp file
         temp = USER_TEMPS_PATH + str(user.getKey()) + ".done"
         if os.path.isfile(temp): # report file exists
            data = None
            with open(temp, 'rb') as expFile:
               data = pickle.load(expFile)
            current = int(tm.time())
            if current < data["endTime"]: # not completed
               remain = timeString(data["endTime"] - current)
               await waitThenSend(ctx,
                  "`{}` until end of your exploration {}.".format(remain,
                     mention))
            else: # completed
               # two cases based on data['cleared']
               if data["cleared"]: # success
                  for u in data["users"]:
                     u.getHero().resurrect() # resurrect hero if needed
                     # rescue fallen adventurer
                     rewards = await rescueFallen(u.getRescueKey(), 
                        data["floor"])
                     report = data["report"]
                     if rewards != None:
                        report += "rescue rewards: "
                        for i, (itm, q) in enumerate(rewards):
                           u.getHero().getBag().addMulti(itm, q)
                           report += itm.getName() + " x " + str(q)
                           if i < len(rewards) - 1:
                              report += ", "
                     u.setRescueKey(0) # reset rescue key
                     u.inCity = True # set as in town
                     u.setKey(0) # reset exploration key
                     u.setTopFloor(data["floor"]) # update top
                     recoverData(u) # keep important data before overwriting
                     # overwrite/update user account and hero
                     save(u)
                     await (await getDM(u)).send(report) # dm
                  os.remove(temp) # erase temp file
               else: # failure
                  # in case of failure, the player(s) hero(es) is(are) 
                  # stuck in the dungeon until rescued.
                  # rename ".wait" into a ".resq"
                  os.rename(temp, 
                        USER_TEMPS_PATH + str(user.getKey()) + ".resq")
                  # send the DMs
                  name = data["file"]
                   # change extension to .txt
                  name = name.split('.')[0] + ".txt"
                  os.rename(data["file"], name)
                  # send failure DMs
                  for u in data["users"]:
                     await (await getDM(u)).send(data["report"],
                        file = discord.File(name)) # dm
                  os.remove(name) # delete failure file
               # announce to the user(s) to check their DM
               await waitThenSend(ctx, 
                     mention + " check your DMs for the report.")
         else: # ".done" file doesn't exist
            temp = USER_TEMPS_PATH + str(user.getKey()) + ".resq"
            if os.path.isfile(temp): # ".resq" exists
               msg = "your party has fallen {}. ".format(mention)
               msg += "use the key {} to ask for help.".format(
                  user.getKey())
               await waitThenSend(ctx, msg)
            else: # problem with exploration
               # so we free the user
               user.setKey(0)
               user.inCity = True
               save(user)
               msg = "something went wrong. your hero comes back "
               msg += "to the city {}".format(mention)
               await waitThenSend(ctx, msg)

# take on a rescue mission
@bot.command(name = "rescue", help = "use this command and pass it the "
   "key of the fallen party to go rescue them.\neg.: "
   "`;rescue 1234567890`")
async def getRescueKey(ctx, key: str):
   '''set this player's rescue attribute to the key passed so that
   they can attempt a rescue in the next exploration.'''
   if (await isRegisteredWithHero(ctx)):
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      resq = USER_TEMPS_PATH + str(key) + ".resq"
      if os.path.isfile(resq): # fallen party exist
         user.setRescueKey(key) # set rescue key
         save(user) # to record key
         floor = 0
         with open(resq, "rb") as rescueFile:
            contents = pickle.load(rescueFile)
            floor = contents["floor"]
         msg = "{}, you're set to go rescue a fallen party on `floor {}`".format(
            mention, floor)
         msg += ". make sure to explore that floor immediatly."
         await waitThenSend(ctx, msg)
      else: # wrong key?
         await waitThenSend(ctx, 
            "your key doesn't seem valid {}...".format(mention))

# automatic rescue of fallen character
@bot.command(name = "saveme", help = "pay a stipend to get your hero "
   "rescued from his fallen party. if the party has other heroes "
   "in it, this will only save you, not the others. the party "
   "will stay fallen untill all the other heroes have been saved.\n"
   "eg.: `;saveme`"
)
async def saveme(ctx):
   '''rescue the user's avatar for the floor's danger level * 20 coins
   fee.'''
   if (await isRegisteredWithHero(ctx)):
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      resq = USER_TEMPS_PATH + str(user.getKey()) + ".resq"
      msg = str()
      if (not user.isInCity()) and os.path.isfile(resq): # fallen party exists
         # recover data
         data = None
         with open(resq, "rb") as file:
            data = pickle.load(file) 
         idx = 0
         found = False
         while idx < len(data["users"]) and not found:
            found = data["users"][idx].getUname() == user.getUname()
            if not found:
               idx += 1
         if found: # user is in party
            fee = DUNGEON[data["floor"]].getHazardLevel() * 20
            paid = user.getHero().getWallet().pay(fee)
            if paid != None: # payment successful
               # free user
               user.inCity = True
               user.setKey(0)
               save(user)
               # update rescue file
               data["users"].remove(data["users"][idx])
               if len(data["users"]) > 0: # there's other heroes
                  with open(resq, "wb") as file:
                     data = pickle.dump(file, pickle.HIGHEST_PROTOCOL)
               else:
                  os.remove(resq) # erase rescue file
               # send a response message
               msg += "an elite team from the city went to save your "
               msg += "ass for `{} coins` {}. ".format(fee, mention)
               msg += "now be careful."
            else: # couldn't pay
               msg += "it costs `{} coins` to do a rescue there {}. ".format(
                  fee, mention)
               msg += "you don't have that kind of money."
         else: # user was not in party
            # error? so free uer
            user.setKey(0)
            user.inCity = True
            save(user)
            # send message
            msg += "{} you don't need rescue.".format(mention)
      else:
         msg += mention + ", you are "
         if user.isInCity():
            msg += "safe and sound in the city right now."
         else: 
            msg += "you were last seen heading on an exploration."
            msg += "use `;report` to check the exploration status."
      await waitThenSend(ctx, msg)

# check items
@bot.command(name = "lookup", help = "check an owned item info. the "
   "item must be in your bag for this to work. if the item name is "
   "composite, you must put the name in between `quotes (" ")`. "
   "eg.: `;lookup arrow`\n`;lookup \"iron ore\"`.")

async def lookup(ctx, itemName: str):
   '''checks hero bag for an item of the same name. if found,
   return a detailed view of the item.'''
   if (await isRegisteredWithHero(ctx)):
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      # check if the player owns the item
      if user.getHero().getBag().contains(itemName):
         page = discord.File(pg.genItem(user, itemName))
         await ctx.send("{} this item is:".format(mention), 
            file = page)
      else:
         await waitThenSend(ctx,
            "{} you don't have any item of that name in your bag.".format(
            mention))

# reveal ID
@bot.command(name = "myplayerid", help = "request your ID to use when "
   "someone is trying to add you to their friendbook. if you don't "
   "add a friend, then the ID will be DM'd to you.\n"
   "eg.: `;myplayerid frid1234` or `;myplayerid`"
)
async def myplayerid(ctx, fuid: str=None):
   '''DM the sender their ID. if the friend attribute is passed, 
   the id is send directly to the friend if they are in your 
   friendbook.'''
   if fuid == None:
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      id = ctx.message.author.id
      msg = "your ID is in the next message."
      msg += ":warning: "
      msg += "**make sure you share this only with people you trust.** "
      msg += ":warning:"
      await (await getDM(user)).send(msg)
      await (await getDM(user)).send( "**{}**.\n".format(id))
      await waitThenSend(ctx, "check your DM {}".format(mention))
   else: # a valid friend
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      id = ctx.message.author.id
      friend = user.getFriendBook().getFriend(fuid)
      if friend != None: # entry exists in friendbook
         friend = load(friend[0])
         msg = "{} wants you to add them as a friend. ".format(
            user.getUname())
         msg += "copy, paste and send the next message to add them."
         await (await getDM(friend)).send(msg)
         command = ";befriend {}".format(id)
         await (await getDM(friend)).send(command)
         await waitThenSend(ctx, "{}, invite was sent.".format(mention))
      else: # entry doesn't exists
         msg = "there's no friend of by that name in your friendbook"
         msg += " {}.".format(mention)
         await waitThenSend(ctx, msg)

# make friends
@bot.command(name = "befriend", help = "provide the id of the user "
   "that you want to befriend. if valid, they will be added to your "
   "friendbook. you can then invite them to exploration anytime "
   "they are available for coop.\n"
   "eg.: `;befriend 1232343434535`.")
async def addFriend(ctx, fID: int):
   '''check if any hero save matches the passed username. if
   so, add them as friend.'''
   if (await isRegisteredWithHero(ctx)):
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      if isRegistered(fID): # a player with that id exists
         if fID != user.getID(): # can't add yourself
            friend = load(fID)
            fuid = user.getFriendBook().addFriend(fID,
               friend.getUname())
            if fuid != None: # add successful
               save(user)
               msg = "say hi to your new friend **{}** ".format(fuid)
               msg += "you can use the `friendbook` command to check "
               msg += "on all your friends anytime."
            else: # add not successful
               msg = "you already have them as friend {}.".format(
                  mention)
            await waitThenSend(ctx, msg) # response
         else:
            await waitThenSend(ctx,
               "you can't befriend yourself {}.".format(mention))
      else: # friend isn't a registered player
         await waitThenSend(ctx, "Couldn't find friend.")

# check friendbook
@bot.command(name = "friendbook", help = "prints a list of the "
   "contents of your friendbook.\neg.: `;friendbook`")
async def friendbook(ctx):
   '''unveils the contents of the user friendbook.'''
   id = ctx.message.author.id
   if isRegistered(ctx.message.author.id):
      user = load(id)
      fb = user.getFriendBook().__str__()
      await waitThenSend(ctx, fb)
   else:
      mention = ctx.message.author.mention
      await waitThenSend(ctx, mention)

# toggle coop
@bot.command(name = "coop", help = "toggle the value of your open "
   "attribute. if true, you will be available for coop explorations. "
   "else, no one will be able to drag you on exploration with them.\n"
   "eg.: `;coop1`")
async def coop(ctx):
   '''toggle the user's open attribute.'''
   id = ctx.message.author.id
   mention = ctx.message.author.mention
   if isRegistered(ctx.message.author.id):
      user = load(id)
      user.open = not user.isOpen()
      msg = "{}".format(mention)
      if user.isOpen(): # activated coop
         msg += " you are now available for coop. your profile "
         msg += "page will show a :green_circle: under `Open`."
      else:
         msg += " you are now unavailable for coop. your profile "
         msg += "page will show a :red_circle: under `Open`."
      save(user)
      await waitThenSend(ctx, msg)
   else:
      await waitThenSend(ctx, nRegMSG.format(mention))

# show available merchandise
@bot.command(name = "shop", help = "reveals the items that are for "
   "sale at the moment.\neg.: `;shop`")
async def shop(ctx):
   '''shows wares available in online shop.'''
   if (await isRegisteredWithHero(ctx)): # only the hero has a bag
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      # TODO randoms = []
      # make wares
      wares = [spawner() for spawner in ALWAYS]
      # shopkeep lines
      msg = "shopkeep: "
      lines = [
         "Oh {}? coming to buy stuff again? when do you make the "
         "money?\n",
         "*Welcome to my hum... oh it's just you {}.\n",
         "I am having sales today {}. everything is double the "
         "normal price!\n",
      ]
      msg += rnd.choice(lines)
      msg = msg.format(mention)
      msg += "\nhere is what is available today:"
      # message is embed now
      shop = discord.Embed(
         title = "Shop",
         url = "",
         description = msg,
         color = discord.Color.purple()
      )
      for i, ware in enumerate(wares):
         field = ware.getLore()
         # gear?
         if isinstance(ware, (c.Gear)):
            msg += ware.overview()
         field += " `price`: **{}** gold".format(ware.getValue())
         if ware.getValue() > 1:
            msg += 's'
         # add to embed
         shop.add_field(
            name = ware.getName(),
            value = field,
            inline = (i % 2) == 0 # inline is on for every even ware
         )
      # sassy ending lines
      footer = "\nshopkeep: "
      ends = [
         "so ya buying or ya leaving?\n",
         "now put those coins where I can see 'em!\n"
      ]
      footer += rnd.choice(ends)
      shop.set_footer(text = footer)

      # send out
      await ctx.send("{}".format(mention),
         embed = shop,
         file = discord.File(pg.PAGES + "shopkeep.jpg")
      )
      #await waitThenSend(ctx, msg)
   
# buy from server shop
@bot.command(name = "buy", help = "buy something from the bot server "
   "shop. requires that you pass the name of the item as an argument."
   " only works if you are a register user with a hero and if you "
   "have sufficient funding. you can specify the quantity if you "
   "want more than one. you need to use quotes if item name is "
   "composite.\n"
   "eg.: ;buy shoes or ;buy \"small bag\" or ;buy arrow 50 ")
async def buy(ctx, itemName, qty: int=None):
   '''checks if the item is available then check if the user has
   the necessary funds. takes the funds and give them the necessary
   amount requested.'''
   if qty == None:
      qty = 1 # only wants one
   if (await isRegisteredWithHero(ctx)): # only the hero has a bag
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      if user.isInCity():
         msg = "shopkeep: "
         # spawn items
         wares = [spawner() for spawner in ALWAYS]
         # check if item requested exists
         names = [(ware.getName()).lower() for ware in wares]
         itemName = itemName.lower()
         if itemName in names: # item exists
            i = names.index(itemName)
            item = wares[i]
            # check if user has the funds
            price = item.getValue()
            paid = user.getHero().getWallet().pay(price * qty)
            if paid != None: # funds were paid
               # check if user can pocket the item
               if user.getHero().getBag().hasSpace():
                  # we are good
                  bag = user.getHero().getBag()
                  bag.addMulti(item, qty)
                  save(user) # record purchase
                  msg += "*Hehe thanks for the money {}. ".format(mention)
                  msg += "Oh and I don't do guaranty or shit. best of "
                  msg += "luck. Hehehe~*"
               else:
                  msg += "*What you don't have no space for it {}? "
                  msg += "Well I would keep the money but...*".format(mention)
            else: 
               msg += "*Nah {} you can't afford this.*".format(mention)
         else:
            msg += "*Are you blind? Do you see that anywhere in here {}?*"
            msg = msg.format(mention)
      else:
         msg = "{} you can only buy when you are in town.".format(mention)
      # end of buy algorithm
      await waitThenSend(ctx, msg) # send sassy response

# sell loot
@bot.command(name = "sell", help = "allows the player to sell loot "
   "they own to the server shop. that's the easiest way to earn "
   "money. note that the base selling price is only half the "
   "good's value but with **luck** you can haggle a better "
   "price.\neg.: ;sell pelt or ;sell \"small feathers\" or "
   ";sell violette 5")
async def sell(ctx, itemName: str, qty: int=1):
   '''checks for the existence of the specified item and bargains
   them to the shop owner. return the money earned from selling'''
   if qty == None:
      qty = 1 # only sells one
   if (await isRegisteredWithHero(ctx)): # only the hero has a bag
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      if user.isInCity(): # can only sell when in town
         bag = user.getHero().getBag()
         msg = "shopkeep: "
         if bag.contains(itemName): # we have the item:
            sales = bag.takeOut(itemName, qty)
            if len(sales) == qty: # enough items            
               uPrice = sales[0].getValue(True) # get unit selling price
               if uPrice < 1:
                  uPrice = 1
               luck = user.getHero().getStats().getStat("luck")
               luck = luck.getFull()
               # get a haggle bonus
               haggle = rnd.randrange(luck) * .1 + 1
               total = ceil(uPrice * haggle * len(sales))
               msg += "*Herh. Alright I guess you earned this one.*\n"
               msg += "{} **receive {} gold".format(mention, total)
               if total > 1:
                  msg += 's'
               msg += "**"
               user.getHero().getWallet().pocket(total)
               save(user)
            else: # not enough.
               msg += "*Who taught you how to count {}?*".format(mention)
         else:
            msg += "*hum... But I don't see the goods you mention {}.*"
            msg = msg.format(mention)
      else:
         msg = "{} you can only sell when you are in town.".format(mention)
      await waitThenSend(ctx, msg)

# equip gear
@bot.command(name = "equip", help = "equip any gear you possess in "
   "your bag at the moment. gear gets automatically placed where "
   "it can be equipped. any gear previously equipped there will "
   "be return to you. gear of composite name should be specified "
   "in between quotes.\neg.: ';equip sword' or ';equip \"long lance\"'"
   )
async def equip(ctx, gearName):
   '''equip the passed gear.'''
   if (await isRegisteredWithHero(ctx)): # only the hero has a bag
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      msg = "{} ".format(mention)
      if user.isInCity(): # can only equip when in town
         bag = user.getHero().getBag()
         if bag.contains(gearName): # item exists
            gear = bag.takeOut(gearName)[0]
            if isinstance(gear, c.Gear): # a gear
               # equip it
               old = user.getHero().getEquipped().setGear(gear)
               if old != None:
                  bag.add(old) # return old equipment
                  msg += "takes off `{}` and ".format(old.getName())
               msg += "equips `{}`.".format(gear.getName())
               save(user)
            else:
               msg += "you can't equip that!"
         else:
            msg += "you don't own that!"
      else:
         msg += "you can only equip gear when you are in town."
      await waitThenSend(ctx, msg)

# set skills
@bot.command(name = "skillset", help = "set a skill in one of the "
   "skill slot of your hero. possible skill slots are <a> (Ability), "
   "<r> (Reaction) and <c> (Critical). the base skill can never be "
   "changed. "
   "only learned skills can be set and a skill can only be set. "
   "all learned skills can be seen using the ';learned' command.\n"
   "eg.: ';skillset a cleaver' or ';skillset r counter'"
   )
async def skillset(ctx, slot: str, skillName: str):
   '''equip the passed skill.'''
   if (await isRegisteredWithHero(ctx)): # only the hero has a bag
      user = load(ctx.message.author.id)
      mention = ctx.message.author.mention
      msg = "{} ".format(mention)
      skillName = skillName.lower()
      aLevel = user.getHero().getLevel().getCurrent()
      mastery = user.getHero().getMastery()
      if user.isInCity(): # can only equip when in town
         uLevel = mastery.getUnlockLevel(skillName)
         print(uLevel, aLevel)
         if uLevel != -1 and uLevel <= aLevel: # learned it
            skill = mastery.getSkill(uLevel, aLevel)
            skillset = user.getHero().getSkillSet()
            if uLevel == 0: 
               # trying to reequip base
               msg += "base skills can't be reassigned."
            else:
               slot = slot.lower()
               if not (slot in ['a', 'r', 'c']):
                  msg += "invalid slot. the only available slots "
                  msg += "are `a` (ability), `r` (reaction) and `c` "
                  "(critical)."
               else: # we are good
                  if slot.lower() == 'a':
                     slot = "Ability"
                  elif slot.lower() == 'r':
                     slot = "Reaction"
                  else:
                     slot = "Critical"
                  done = skillset.assign(slot.lower(), skill)
                  # print(done) # DEBUG
                  msg += "**{}** is now your new ".format(skill.getName())
                  msg += slot
                  msg += " skill."
                  save(user)
         else:
            msg += "you haven't learned that skill."
      else:
         msg += "you can only change skills when you are in town."
      await waitThenSend(ctx, msg)

# test command
@bot.command(name = "test", help = "for development purposes.")
async def test(ctx, other = None):
   '''used to try out library methods and other.'''
   await waitThenSend(ctx, 
      "*No beta function available at the moment.*")  
   ''' # resq file check
   await waitThenSend(ctx, 
      "check the console developer-san.")  
   with open(USER_TEMPS_PATH + "1633746541.resq", "rb") as file:
      data = pickle.load(file)
      print(data)
   '''

# run module
if __name__ == "__main__":
   # check for existence of required repos structure
   if not os.path.exists("records/"):
      os.mkdir("records")
      for subRep in ["generated", "pics", "saves", "temps", "users"]:
         os.mkdir("records/" + subRep)
   # run bot / catch and log errors
   try:
      bot.run(os.getenv("BOT_TOKEN"))
   except: # catch any occurence
      logError(sys.exc_info())
