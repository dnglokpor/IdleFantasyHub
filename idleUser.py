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
      self.inCity = True
      self.available = True
      self.topFloor = 0
      self.picture = str() # path to profile pic
   
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
      return self.inCity == True
   def isAvailable(self) -> bool:
      '''True if self.available evaluates to True.'''
      return self.available == True
   def getTopFloor(self) -> int:
      return self.topFloor
   def getPicture(self) -> str:
      '''return the path to the class icon.'''
      return self.picture
      
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
      return descr
      
# records
USER_RECORDS_PATH = "records/users"
HERO_SAVES_PATH = "records/saves"
USER_PICS_PATH = "records/pics"
   
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
   userfile = USER_RECORDS_PATH + '/' + str(id) + '.usr'
   herofile = HERO_SAVES_PATH + '/' + str(uname) + '.her'
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
   # picture
   user.picture = lines[4].split()[1]
   return user