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
try:
   import cPickle as pickle              # pickle
except ModuleNotFoundError:
   import pickle
from glob import glob
from idleUser import IdleUser, save, load


# add game world package to path so that internal imports work
sys.path.insert(0, os.getcwd() + "/world")

import world.skillLib as skl

USERS_FILES = "records/users/"
HERO_FILES = "records/saves/"

# update function
def masteryUpdate():
   '''update hero's mastery objects'''
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
         except Exception:
            data = sys.exc_info() # information on error
            print("error updating ", file)
            print(data)
   else:
      print("Directory ", USERS_FILES, "not found.")
      
def pickleProtocoleUpdate():
   '''change the pickle protocole of hero files.'''
   if os.path.exists(HERO_FILES): # folder exists
      sQueue = glob(HERO_FILES + "*.her") # update queue
      print("all files: ", sQueue, "\n\n") # DEBUG
      for file in sQueue:
         try:
            pickled5 = None
            # recover data
            with open(file, "rb") as savefile: 
               pickled5 = pickle.load(savefile)
            # write back
            with open(file, "wb") as savefile:
               pickle.dump(pickled5, savefile)
         except Exception:
            print("failed to update ", file, "\n")
            data = sys.exc_info() # information on error
            print("error updating ", file)
            print(data)
      
if __name__ == "__main__":
   # masteryUpdate()
   pickleProtocoleUpdate()