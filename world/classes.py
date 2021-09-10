'''
# classes.py
# contains the definition of all the two different Monster
# and Adventurer objects. these are the final subclasses
# of units that should actually be spawned and used.
# date: 7/4/21
# author: dnglokpor
'''

# imports 
from elements import Element, NOELM 
from base import UnitStats
from units import Unit, Playable
from skills import Skill, SkillSet, Mastery
from skillLib import blademanship, survivalist, conjuring
from itemLib import arrow, longsword, longbow, walkingStick,\
   goGetup
from random import choice
from math import ceil

# Monster object
class Monster(Unit):
   '''a subclass of a Unit object. this represent a non-
   abstract monster which adds to units characteristics
   the skills it takes to defeat adventurers. scales
   up stats by a factor of half the level thus the stats
   list provided should be what it would have been at level
   1.'''
   
   def __init__(self, name: str, level: int, bStats: list,
      bSkill: Skill, lore: str, elt = NOELM):
      super().__init__(name, level,
         [stat * level for stat in bStats], 3, elt)
      self.lore = lore
      self.skillSet = SkillSet(bSkill)
   
   # getters
   def getSkillSet(self) -> SkillSet:
      '''return the SkillSet object of the monster'''
      return self.skillSet
   def getLore(self) -> str:
      '''return the lore surrounding this Monster.'''
      return self.lore
   
   # setters
   # all skills can be set by getting the SkillSet object
   
   # skills usage
   def act(self, state):
      '''calls the best action available between the base
      skill and the ability skill.'''
      action = self.skillSet.getBestAction()
      return action(self, state)
   def react(self, state):
      '''calls upon the reaction skill.'''
      reaction = self.skillSet.getSkill("reaction")
      return reaction(self, state)
   def react(self, state):
      '''calls upon the critical skill.'''
      critical = self.skillSet.getSkill("critical")
      return critical(self, state)
   
   # override tostring
   def __str__(self, short = True):
      '''return a string representing this object for
      printing purposes.'''
      if short:
         return super().__str__()
      description = "{} <Monster>:".format(self.name)
      description += '\n' + self.lore
      return description

# Adventurer object
class Adventurer(Playable):
   '''a subclass of Playable that represent a hero of
   IdleFantasyHub. to the basics of a Playable, add
   a skillSet and also a Mastery. an Adventurer
   is always created at level 1. will be inherited 
   and instantiated through job classes.'''
   
   def __init__(self, cName: str, uName: str, bStats: list,
      mastery: Mastery, lore: str, elt = NOELM):
      super().__init__(uName, 1, bStats, elt)
      self.className = cName
      self.mastery = mastery
      # basic skill is skill unlocked at level 1 of mastery
      self.skillSet = SkillSet(self.mastery.getBase())
      self.lore = lore
   
   # getters
   def getClassName(self) -> str:
      '''return the name of this adventurer job.'''
      return self.className
   def getSkillSet(self) -> SkillSet:
      '''return the SkillSet object of the adventurer'''
      return self.skillSet
   def getMastery(self) -> Mastery:
      '''return the Mastery object of the adventurer'''
      return self.mastery
   def getLore(self) -> str:
      '''return the lore surrounding this adventurer'''
      return self.lore
   
   # skills usage
   def act(self, state):
      '''calls the best action available between the base
      skill and the ability skill.'''
      action = self.skillSet.getBestAction()
      return action(self, state)
   def react(self, state):
      '''calls upon the reaction skill.'''
      reaction = self.skillSet.getSkill("reaction")
      return reaction(self, state)
   def react(self, state):
      '''calls upon the critical skill.'''
      critical = self.skillSet.getSkill("critical")
      return critical(self, state)
   
   # override tostring
   def __str__(self, short = True):
      '''return a string representing this object for
      printing purposes.'''
      if short:
         return super().__str__()
      description = "{} <{}>:".format(self.name, self.className)
      description += '\n' + self.lore
      return description

# helpers
def rndLuck(max = 10):
   '''randomly allocates a number between 1 and max for
   the luck stat.'''
   return choice(range(max)) + 1

# Predefined Jobs
# TBD include default gear assignment in constructor
# Fighter Job
class Fighter(Adventurer):
   '''a Fighter is a basic adventurer class with all-round
   good physicals and a proficient in weapon handling.
   derives from Adventurer but adds a restriction on
   equipment as well as physical development at level up.'''
   
   def __init__(self, uName: str):
      # build adventurer
      super().__init__(
         "Fighter",
         uName, 
         [45, 15, 13, 9, 8, 10, rndLuck()], 
         blademanship,
         "adventurer class with all-round good physicals\
 and a proficient in bladed weapon handling. monsters might\
 enjoy hitting them but they usually get hit back harder.", 
         elt = NOELM
      )
      # default gear
      #self.equip(longsword)
      self.equip(goGetup)
 
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
            # luck increases by at most 3
            newStats[6] += rndLuck(3)
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
         [40, 13, 12, 8, 7, 15, rndLuck()],
         survivalist,
         "veteran of dungeons, rangers use their light steps\
 to explore swiftly and dodge with finesse. armed with their\
 favorite ranged weapon, they patrol the wilderness.", 
         elt = NOELM
      )
      # default gear
      self.equip(longbow)
      self.equip(goGetup)
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
            # luck increases by at most 3
            newStats[6] += rndLuck(3)
         # assign new stats
         self.stats = UnitStats(newStats)
      return lvlGain[0]

# Ranger Job
class Elementalist(Adventurer):
   '''Elementalists perform the best at arcanes which
   allows them to conjure elemental magic. derives from
   Adventurer but adds a restriction on equipment as well
   as physical development at level up.'''
   
   def __init__(self, uName: str):
      # build adventurer
      super().__init__(
         "Elementalist", 
         uName, 
         [40, 9, 10, 15, 13, 8, rndLuck()], 
         conjuring,
         "they say dungeons just like magic sip into this world\
 from a distant place. that might explain how rare the\
 talent of conjuring and wielding elements is.", 
         elt = NOELM
      )
      # default gear
      self.equip(walkingStick)
      self.equip(goGetup)
 
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
            # luck increases by at most 3
            newStats[6] += rndLuck(3)
         # assign new stats
         self.stats = UnitStats(newStats)
      return lvlGain[0]