'''
# idleUser.py
# this contains the declaration of the object that will be 
# used to record instances of player of the game. it became
# necessary to separate this from the bot's main program
# for exportability reason.
# date 10/01/21
# author: dnglokpor
'''

# imports
import sys, os
import random as rnd
try:
   import cPickle as pickle              # pickle
except ModuleNotFoundError:
   import pickle

# add game world package to path so that internal imports work
sys.path.insert(0, 
   "D:/myLewysG/Logiciels/Mes Tests/IdleFantasyHub/world")
from world.classes import Adventurer

# helpers
def boolEvaluate(string: str):
   '''return a boolean value that matches the passed
   string. defaults to false.'''
   if string.lower() == "true":
      return True
   else:
      return False


# Friendbook object
class Friendbook(dict):
   '''a friendbook is a record of all registered players that
   you want to be able to do IdleFantasyHub activities with.
   in practice, every new entry gets given a unique ID that
   you can use to invite them afterward.'''
   def __init__(self):
      super().__init__()
      self.seed = rnd.randrange(9999) + 1 # uid incrementor
   
   # getters
   def getFriend(self, fuid: str):
      '''return the IdleUser ID, uname of your friend if he is
      in the book.'''
      friend = None
      if self.__contains__(fuid):
         friend = self.get(fuid)
      return friend
   
   # setters
   def addFriend(self, id: int, uname: str):
      '''add a new entry to the friendbook.'''
      # make fuid
      fuid = uname[:4].lower()
      while len(fuid) < 4: # uname of less than 4 characters
         fuid += '_' # fill to 4 with underscores
      fuid += str(self.seed) # add counter current value
      seed += 1 # increment counter
      self[fuid] = (id, uname)
   def setSeed(self, seed: int):
      '''allow to set seed in case the Friendbook must be
      reconstructed.'''
      self.seed = seed
   def restoreEntry(self, fuid: str, id: int, uname: str):
      '''allows entries to be entered without a key to be generated.'''
      self[fuid] = (id, uname)
   
   # string for file writing
   def outStream(self) -> str:
      '''transform this object into a string that is easy to parse.'''
      string = "Friendbook {} {}".format(self.seed, len(self.values()))
      for fuid, entry in self.items():
         string += fuid + ' ' + entry[0] + " " + entry[1]
         string += '\n'
      return string
      
   # toString
   def __str__(self) -> str:
      '''return the whole content of the phonebook as a string.'''
      string = "**Discord User**\t**COOP Avail.**\t**FID**"
      for i, (id, entry) in enumerate(self.items()):
         user = load(entry[0], entry[1])
         available = user.isInCity() and user.isAvailable() and user.isOpen()
         if available:
            available = ":green_circle:"
         else:
            available = ":red_circle:"
         string += "`@{}`\t``\t`{}`".format(entry[1], available, id)
         if i < len(self.values()) - 1:
            string += '\n'
      return string
   
# IdleUser object
class IdleUser:
   '''this class records information about the users that
   interact with the bot so they can be remembered.
   provides a way to write this info to the disc.'''
   def __init__(self, id: int, uname: str):
      '''only requires those to create the object. other
      attributes will be set later.'''
      self.id = id
      self.uname = uname
      self.hero = None
      self.inCity = True # in town
      self.available = True # free
      self.topFloor = 0
      self.picture = str() # path to profile pic
      self.key = 0 # key for exploration files
      self.open = False # open to exploring with others
      self.rescue = 0 # key of party to rescue
      self.friendbook = Friendbook() # friendbook
   
   # getters
   def getUname(self) -> str:
      return self.uname
   def getID(self) -> int:
      return self.id
   def hasHero(self) -> bool:
      return self.hero != None
   def getHero(self) -> Adventurer:
      return self.hero
   def isInCity(self) -> bool:
      '''True if self.inCity evaluates to True.'''
      return self.inCity
   def isAvailable(self) -> bool:
      '''True if self.available evaluates to True.'''
      return self.available
   def isOpen(self) -> bool:
      '''return True if self.open == True.'''
      return self.open
   def getTopFloor(self) -> int:
      return self.topFloor
   def getPicture(self) -> str:
      '''return the path to the class icon.'''
      return self.picture
   def getKey(self) -> int:
      '''return the key of the user'''
      return self.key
   def getRescueKey(self) -> int:
      '''return the key of the user to rescue.'''
      return self.rescue
   def getFriendBook(self) -> Friendbook:
      '''return the Friendbook object of this user.'''
      return self.friendbook
   def isFreeTo(self) -> bool:
      '''return True if the user is inCity and available.'''
      return self.inCity and self.available
   def canCoop(self) -> bool:
      '''return True if the user is available to coop.'''
      return self.isFreeTo() and self.open
      
   # setters: most attributes can be used directly
   def setPic(self, path: str):
      '''checks if the passed path is an existing file in which
      case it is set as icon path else raise ValueError.'''
      if not os.path.isfile(path):
         raise ValueError("<{}> path is invalid!".format(path))
      # else
      self.picture = path
   def setHero(self, adv: Adventurer):
      '''set the hero attribute to the Adventurer object
      it represents.'''
      self.hero = adv
   def setTopFloor(self, floor: int):
      '''if the floor > self.topFloor then we make floor
      the new top.'''
      if floor > self.topFloor:
         self.topFloor = floor
   def setKey(self, val: int):
      '''set the key value. this is needed to recover exploration
      status.'''
      self.key = val
   def setRescueKey(self, val: int):
      '''set the key value for a rescue. this is needed to free
      players that fell on exploration.'''
      self.rescue = val
   
   # toString
   def __str__(self) -> str:
      '''creates a string that describe the object.'''
      descr = "Idle Fantasy User:\n"
      descr += "id {}\n".format(self.id)
      descr += "username {}\n".format(self.uname)
      descr += "hero {}\n".format(self.hasHero())
      descr += "city {}\n".format(self.inCity)
      descr += "available {}\n".format(self.available)
      descr += "top {}\n".format(self.topFloor)
      descr += "pp_path {}\n".format(self.picture)
      descr += "key {}\n".format(self.key)
      descr += "open {}\n".format(self.open)
      descr += "rescue {}\n".format(self.rescue)
      descr += self.friendbook.outStream()
      return descr
      
# records
USER_RECORDS_PATH = "records/users/"
HERO_SAVES_PATH = "records/saves/"
USER_PICS_PATH = "records/pics/"
USER_TEMPS_PATH = "records/temps/"
   
# records helpers
def save(user: IdleUser):
   '''write the user object to a file in a readable way.
   overwrite the file if it already exists.'''
   # create the file
   userfile = USER_RECORDS_PATH + '/' + str(user.id) + '.usr'
   herofile = HERO_SAVES_PATH + '/' + str(user.uname) + '.her'
   # write user info to a file
   with open(userfile, "w+") as record:
      record.write(user.__str__())
   # write avatar to file
   if user.hasHero(): # an avatar is tied to this account
      with open(herofile, "wb") as save:
         pickle.dump(user.hero, save, pickle.HIGHEST_PROTOCOL)
   return True      

# load user data
def load(id: int, uname: str) -> IdleUser:
   '''looks for the user save file and create a user object
   that matches it and return it. if the hero value is True,
   look for the hero save file, loads it and add it to the
   user item. return said item. this assumes the user file
   exists already.'''
   userfile = USER_RECORDS_PATH + str(id) + '.usr'
   herofile = HERO_SAVES_PATH + str(uname) + '.her'
   # recover user file contents
   with open(userfile, "r") as record:
      contents = record.read()
   lines = contents.split('\n')
   lines = lines[3:] # delete title line through id line
   # recreate user object
   user = IdleUser(id, uname)
   # hero
   if boolEvaluate(lines[0].split()[1]): # there is a hero
      with open(herofile, "rb") as save:
         user.hero = pickle.load(save)
   else:
      user.hero = None
   # other
   user.inCity = boolEvaluate(lines[1].split()[1])
   user.available = boolEvaluate(lines[2].split()[1])
   user.topFloor = int(lines[3].split()[1])
   user.picture = lines[4].split()[1]
   user.key = int(lines[5].split()[1])
   user.open = boolEvaluate(lines[6].split()[1])
   user.rescue = int(lines[7].split()[1])
   friendbook = lines[8].split()
   user.friendbook.setSeed(friendbook[1]) 
   n = int(friendbook[2])
   i = 0
   while i < n:
      data = lines[9 + i].split()
      user.friendbook.restoreEntry(data[0], data[1], data[2])
   return user