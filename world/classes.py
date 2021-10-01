'''
# classes.py
# contains the definition of all the two different Monster
# and Adventurer objects. these are the final subclasses
# of units that should actually be spawned and used.
# date: 7/4/21
# author: dnglokpor
'''

# imports 
from helpers import rndGen
from base import UnitStats
from elements import NOELM 
from skills import Mastery
from units import Playable
from skillLib import blademanship, survivalist, conjuring
from itemLib import arrow, shortSword, longbow, walkingStick,\
   goGetup, gloves, leatherBoots
from random import choice
from math import ceil

# Adventurer object
class Adventurer(Playable):
   '''a subclass of Playable that represent a hero of
   IdleFantasyHub. to the basics of a Playable, add
   a skillSet and also a Mastery. an Adventurer
   is always created at level 1. will be inherited 
   and instantiated through job classes.'''
   
   def __init__(self, cName: str, uName: str, bStats: list,
      mastery: Mastery, lore: str, elt = NOELM):
      super().__init__(uName, 1, bStats, mastery.getBase(), elt)
      self.className = cName
      self.mastery = mastery
      # basic skill is from mastery is assigned in super call
      self.lore = lore
   
   # getters
   def getClassName(self) -> str:
      '''return the name of this adventurer job.'''
      return self.className
   def getMastery(self) -> Mastery:
      '''return the Mastery object of the adventurer'''
      return self.mastery
   def getLore(self) -> str:
      '''return the lore surrounding this adventurer'''
      return self.lore
   
   # str Output Stream
   def outStream(self):
      '''creates a string that represents the Adventurer in a 
      way that it can be used to rebuild an Adventurer object
      that matches the original.'''
      save = "name {}\n".format(self.uName)
      save += "cName {}\n".format(self.cName)
      save += "totalExp {}\n".format(self.level.getTotalExp())
      save += "stats {}\n".format(self.stats.getFullStats())
      # skill set: skills are optional values
      if self.getSkillSet().getSkill("ability") != None:
         ab = self.getSkillSet().getSkill("ability").getName()
         save += "ability {}\n".format(
            self.mastery.getUnlockedLevel(ab))
      if self.getSkillSet().getSkill("reaction") != None:
         react = self.getSkillSet().getSkill("reaction").getName()
         save += "reaction {}\n".format(
            self.mastery.getUnlockedLevel(react))
      if self.getSkillSet().getSkill("critical") != None:
         crit = self.getSkillSet().getSkill("critical").getName()
         save += "critical {}\n".format(
            self.mastery.getUnlockedLevel(crit))
      # bag: dump a list of the items in the bag in name qty format
      save += "bag"
      for item in self.getBag():
         save += " {} {}".format(item[0].getName(), len(item))
      save += '\n'
      # equipment: pieces are optional values
      if self.getEquipped().getGear("WPN") != None:
         save + "weapon {}\n".format(
            self.getEquipped().getGear("WPN").getName())
      if self.getEquipped().getGear("ARM") != None:
         save + "armor {}\n".format(
            self.getEquipped().getGear("ARM").getName())
      if self.getEquipped().getGear("WPN") != None:
         save + "accessory {}\n".format(
            self.getEquipped().getGear("ACC").getName())
      # wallet
      save += "balance {}\n".format(self.getWallet().getBalance())
      
      # return the string
      return save
         
   # override tostring
   def __str__(self, short = True):
      '''return a string representing this object for
      printing purposes.'''
      description = super().__str__(short)
      if not short:
         description += "class <{}>:".format(self.className)
         description += '\n' + self.lore
      return description

# Predefined Jobs
# TBD include default gear assignment in constructor
# Fighter Job
class Fighter(Adventurer):
   '''a Fighter is a basic adventurer class with all-round
   good physicals and a proficient in melee weapon handling.'''
   
   def __init__(self, uName: str):
      # build adventurer
      super().__init__(
         "Fighter",
         uName, 
         [45, 16, 14, 7, 8, 10, rndGen()], 
         blademanship,
         "adventurer class with all-round good physicals and\n"
         "proficient in bladed weapon handling. monsters \n"
         "might enjoy hitting them but they usually get hit \n"
         "back harder.", 
         elt = NOELM
      )
      # default gear
      self.equip(shortSword)
      self.equip(goGetup)
      self.equip(gloves) # for dev use
 
   # stats development
   def develup(self, expGain: int) -> bool:
      '''absorbs the exp and develop the stats (full
      values) once for every new level gained. development
      only affect the unit's base stats not the combined
      stats taking gear add-ons into account. return
      "True" if a level up occured.'''
      lvlGain = self.getLevel().levelup(expGain)
      if lvlGain[0]: # we have leveled up
         # development branch
         newStats = self.stats.getFullStats()
         dev = [125, 125, 120, 110, 105, 115] 
         for lvl in range(lvlGain[1]): # for each new lvl
            # hp, ..., dext
            newStats = [ceil(newStats[idx] * dev[idx] / 100) \
               for idx in range(6)]
            # append luck to the list
            newStats.append(self.stats.getStat("luck").getFull())
            # luck increases by at most 3
            newStats[6] += rndGen(3)
         # assign new stats
         self.stats = UnitStats(newStats)
      return lvlGain[0]

# Ranger Job
class Ranger(Adventurer):
   '''a Ranger excels in agile movement and deals
   mostly physical damage. derives from Adventurer 
   but adds a restriction on equipment as well as 
   physical development at level up.'''
   
   def __init__(self, uName: str):
      # build adventurer
      super().__init__(
         "Ranger", 
         uName, 
         [40, 13, 12, 8, 7, 15, rndGen()],
         survivalist,
         "veteran of dungeons, rangers use their light steps\n"
         "to explore swiftly and dodge with finesse. armed\n"
         "with their favorite ranged weapon, they patrol the\n"
         "wilderness.", 
         elt = NOELM
      )
      # default gear
      self.equip(longbow)
      self.equip(goGetup)
      self.equip(leatherBoots)
      # startup arrows
      self.getBag().addMulti(arrow, 50)
 
   # stats development
   def develup(self, expGain: int) -> bool:
      '''absorbs the exp and develop the stats (full
      values) once for every new level gained. development
      only affect the unit's base stats not the combined
      stats taking gear add-ons into account. return
      "True" if a level up occured.'''
      lvlGain = self.getLevel().levelup(expGain)
      if lvlGain[0]: # we have leveled up
         # development branch
         newStats = self.stats.getFullStats()
         dev = [120, 120, 115, 110, 110, 125] 
         for lvl in range(lvlGain[1]): # for each new lvl
            # hp, ..., dext
            newStats = [ceil(newStats[idx] * dev[idx] / 100) \
               for idx in range(6)]
            # append luck to the list
            newStats.append(self.stats.getStat("luck").getFull())
            # luck increases by at most 3
            newStats[6] += rndGen(3)
         # assign new stats
         self.stats = UnitStats(newStats)
      return lvlGain[0]

# Ranger Job
class Elementalist(Adventurer):
   '''Elementalists perform the best at arcanes which
   allows them to conjure elemental magic.'''
   
   def __init__(self, uName: str):
      # build adventurer
      super().__init__(
         "Elementalist", 
         uName, 
         [40, 9, 10, 15, 13, 8, rndGen()], 
         conjuring,
         "they say dungeons just like magic sip into this \n"
         "world from a distant place. that might explain how \n"
         "rare the talent of conjuring and wielding elements is.", 
         elt = NOELM
      )
      # default gear
      self.equip(walkingStick)
      self.equip(goGetup)
      self.equip(leatherBoots)
 
   # stats development
   def develup(self, expGain: int) -> bool:
      '''absorbs the exp and develop the stats (full
      values) once for every new level gained. development
      only affect the unit's base stats not the combined
      stats taking gear add-ons into account. return
      "True" if a level up occured.'''
      lvlGain = self.getLevel().levelup(expGain)
      if lvlGain[0]: # we have leveled up
         # development branch
         newStats = self.stats.getFullStats()
         dev = [120, 105, 120, 125, 120, 110] 
         for lvl in range(lvlGain[1]): # for each new lvl
            # hp, ..., dext
            newStats = [ceil(newStats[idx] * dev[idx] / 100) \
               for idx in range(6)]
            # append luck to the list
            newStats.append(self.stats.getStat("luck").getFull())
            # luck increases by at most 3
            newStats[6] += rndGen(3)
         # assign new stats
         self.stats = UnitStats(newStats)
      return lvlGain[0]