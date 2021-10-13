'''
# updater.py
# this module allows the modification of user save files when needed.
# generally, this script will be modified to target the specific
# thing that needs to be updated.
# date: 10/12/21
# author: dnglokpor
'''

# imports
import os
import sys
from glob import glob
from idleUser import IdleUser, save, load

# add game world package to path so that internal imports work
sys.path.insert(0, 
   "D:/myLewysG/Logiciels/Mes Tests/IdleFantasyHub/world")
import world.skillLib as skl

USERS_FILES = "records/users/"
HERO_FILES = "records/saves/"

# update function
def update(user: IdleUser):
   '''multi use function. can be modified for every specific
   use.'''
   # renew the mastery object of the user heroes to include
   # new changes in the object methods.
   hero = user.getHero()
   old = hero.getMastery()
   new = None
   if old.getName().lower() == "blademanship":
      new = skl.blademanship
   elif old.getName().lower() == "survivalist":
      new = skl.survivalist
   else: # conjuring
      new = skl.conjuring
   print("mastery of user [{}] is {}.\n\n".format(user.getUname(),
      new.getName())) # DEBUG 
   hero.mastery = new # reassign new mastery to user

if __name__ == "__main__":
   if os.path.exists(USERS_FILES): # folder exists
      uQueue = glob(USERS_FILES + "*.usr") # update queue
      print("all files: ", uQueue, "\n\n") # DEBUG
      for file in uQueue:
         id = 0
         try:
            with open(file, 'r') as userfile: # recover ID
               lines = userfile.read() # read contents
               # print(lines) # DEBUG
               lines = lines.split('\n') # split into lines
               id = int(lines[1].split()[1]) # extract id
               print("ID: ", id) # DEBUG
               user = load(id) # load user file
               # update function call here
               update(user)
         except Exception:
            data = sys.exc_info() # information on error
            print("error updating ", file)
            print(data)
   else:
      print("Directory ", USERS_FILES, "not found.") 