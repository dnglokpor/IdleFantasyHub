'''
# bg_explorer.py
# this module has only one function. it runs a systematic search
# for files that are related to exploration. the files will be created
# by IdleFantasyBot main process and this background process will
# load them then run the exploration on them and save them back as
# complete.
# author: dnglokpor
# date: 10/5/21
'''

# imports
import sys, os
try:
   import cPickle as pickle
except ModuleNotFoundError:
   import pickle
from glob import glob
import time as tm
from idleUser import USER_TEMPS_PATH

# add game world package to path so that internal imports work
sys.path.insert(0, os.getcwd() + "/world")

from world.confrontation import Party
from world.dungeon import DUNGEON

def run_exploration(file: str):
   '''the unique function of this process. it checks for the existence
   of specific files that tells it if exploration must happen or 
   not. if found, it runs the required exploration and compute the
   results that it then saves back in a file with a different name.
   '''
   # recover data
   setupData = None
   with open(file, "rb") as setupFile:
      setupData = pickle.load(setupFile)
   # shape of the recovered data:
   # setupData = {
   #    "startTime": x,
   #    "floor": x,
   #    "users": [xxx,xxxx,xxxxx]
   # }
   # setup
   f = setupData["floor"]
   start = setupData["startTime"]
   floor = DUNGEON[f]
   blocks = floor.build()
   party = list()
   for u in setupData["users"]:
      party.append(u.getHero())
   party = Party(party)
   hostiles = list() # report
   loot = list() # report
   file = ""
   miscs = "miscellaneous:\n" # report
   # exploration loop
   current = 0
   while current < len(blocks) and party.stillStands():
      block = blocks[current] 
      returned = block.explore(party, floor.getHazardLevel())
      if returned != None:
         for t, descr in returned[0]:
            if t == 'm': # monster
               hostiles.append(descr)
            elif t== 'i': # item
               loot.append(descr)
            else: # miscellaneous
               miscs += "**" + descr + "**\n" # bold
         file = returned[1]
      if party.stillStands():
         current += 1
   # end of exploration loop
   for adv in party.getMembers():
      adv.getSkillSet().resetAll() # reset all skills cooldowns
   cleared = current == len(blocks) # exploration status
   if cleared: # implies party still stands
      report = "Floor {} exploration complete!".format(f)
      report += '\n'
      # hostile report
      report += "monsters encountered: `"
      monsterSet = set(hostiles)
      for i, n in enumerate(monsterSet):
         report += n
         if i < len(monsterSet) - 1:
            report += ", "
      report += "`\n"
      report += "number of monster defeated: `"
      defeated = len(hostiles)
      report += "{}`\n".format(defeated)
      for u in setupData["users"]:
         u.updateDefeated(defeated)
      # loot report
      report += "items found: `"
      itemSet = set(loot)
      for i, n in enumerate(itemSet):
         report += n
         if i < len(itemSet) - 1:
            report += ", "
      report += "`\n"
      report += miscs + '\n'
   else: # party died
      report = "Floor {} exploration failed!\n".format(f)
      report += "your party has fallen...\n"
      report += "your rescue key is **{}**. ".format(
         setupData["users"][0].getKey())
      report += "send it to a friend so they can rescue you.\n\n"
      report += "see attached file for death conditions.\n"
      # last fight info
      # with open(info[1], 'r') as fightInfo:
      #   report += fightInfo.read()
      #os.remove(info[1]) # delete file
   # save all data into one object
   expData = {
      "endTime": start + floor.getSize() * 120 + 1,
      "floor": f,
      "cleared": cleared,
      "users": setupData["users"],
      "report": report,
      "file": file
   }
   # dump object in a file
   with open(USER_TEMPS_PATH + str(start) + ".done", "wb") as expFile:
      pickle.dump(expData, expFile, pickle.HIGHEST_PROTOCOL)
   # erase ".wait"
   os.remove(USER_TEMPS_PATH + str(start) + ".wait")
   
# run
if __name__ == "__main__":
   while(True):
      queue = glob(USER_TEMPS_PATH + "*.wait")
      if len(queue) == 0: # no exploration task waiting
         tm.sleep(10) # sleep 10 sec
      else: # tasks available
         for path in queue:
            run_exploration(path) # run exploration task