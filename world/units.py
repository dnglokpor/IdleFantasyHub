'''
# unit.py
# module that contains all the classes needed to create
# a virtual IdleFantasyHub unit. contains the definition
# of the Unit, Playable and Monster.
# date: 6/25/21
# author: dnglokpor
# update: 9/25/21
# added the BossMonster class which is a list of monsters;
# each representing one form of the boss monster.
'''

# imports
from helpers import rndGen
from base import UnitStats, Gauge
from elements import Element, NOELM
from skills import Skill, SkillSet, EffectList
from containers import Inventory, Equipment, Wallet
from math import ceil

# Unit object
class Unit:
   '''units are abstract base mobs of IdleFantasyHub.
   only units can participate in combat. this class
   provides what is needed to identify and represent
   a unit as well as all characteristics shared by all
   units derivatives.'''
   
   def __init__(self, name: str, level: int, stats: list, 
      bSize: int, bSkill: Skill, elt = NOELM):
      '''if len(stats) is less different from 5, then
      ValueError is raised. a Unit also need
      a way to carry items around. this way, any monster
      can carry its own loot making drops easy to
      determine.'''
      if len(stats) != 7:
         raise ValueError("exactly 7 stats are needed.")
      self.name = name
      self.level = Gauge(level)
      self.element = elt
      self.stats = UnitStats(stats)
      self.skillSet = SkillSet(bSkill)
      self.activeEffects = EffectList()
      self.bag = Inventory(bSize)
   
   # getters:
   def getName(self) -> str:
      '''return unit's name.'''
      return self.name
   def getLevel(self) -> Gauge:
      '''return the level Gauge of the unit.'''
      return self.level
   def getElement(self) -> Element:
      '''return the Element object of the unit.'''
      return self.element
   def getStats(self) -> UnitStats:
      '''return the UnitStats object of the unit.'''
      return self.stats
   def getSkillSet(self) -> SkillSet:
      '''return the SkillSet object of the unit'''
      return self.skillSet
   def getActiveEffects(self) -> EffectList:
      '''return the EffectList object of the unit.'''
      return self.activeEffects
   def getBag(self) -> Inventory:
      '''return the personal inventory of the unit.'''
      return self.bag
   def isAlive(self) -> bool:
      '''return "True" if the unit's current health value
      is above zero. subclasses that add stats bonuses must
      override this method.'''
      return self.stats.getHealth().getCurrent() > 0
   def isCritical(self) -> bool:
      '''return "True" if the unit's health gets under
      a 1/5 of its full value.'''
      full = self.stats.getHealth().getFull()
      cur = self.stats.getHealth().getCurrent()
      return cur < (full // 5)
   
   # setters
   def addLetter(self, order: int):
      '''the "order"th letter of the alphabet after
      'A' to the name of this unit.'''
      self.name += ' ' + chr(ord('A') + order)
   def suffer(self, dmgAmount: int):
      '''reduced the unit's hp by dmgAmount. ignore
      equipment.'''
      self.stats.changeBy("health", -dmgAmount)
   def heal(self, healAmount: int):
      '''raise the unit's hp by healAmount. ignore 
      equipment.'''
      self.stats.changeBy("health", healAmount)
   def resurrect(self):
      '''set the hp of the unit to 1 if they were dead.'''
      if self.isAlive():
         self.heal(1)
      
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = "{} {:2s}".format(self.name,
         self.level.__str__(short))
      if not short: # long description
         description += "\n\nStats:\n"
         description += self.stats.__str__() + '\n'
         description += "\nSkills:\n"
         description += self.skillSet.__str__()
      return description

# Playable object
class Playable(Unit):
   '''a playable is a unit that can be controlled by a
   player of IdleFantasyHub. adds to a basic Unit
   gear slots and a wallet. this allows the Playable
   to have a combined stats attributes that is considered
   its own stat'''
   def __init__(self, name: str, level: int, stats: list,
      bSkill: Skill, elt = NOELM):
      # create underlying Unit
      super().__init__(name, level, stats, 30, bSkill, elt)
      self.equipment = Equipment()
      self.wallet = Wallet(200)     # empty wallet
   
   # getters
   def getEquipped(self) -> Equipment:
      '''get the Equipment attribute of the Playable.'''
      return self.equipment
   def getWallet(self) -> Wallet:
      '''return the Wallet attribute of the Playable.'''
      return self.wallet
   def getStats(self) -> UnitStats:
      '''return the combined stats of the Playable. overrides
      the getStats() method of the Unit class to add bonuses
      from equipped gear.'''
      return (self.stats + 
         UnitStats(self.equipment.getEqtBonus()))
   def isAlive(self) -> bool:
      '''return "True" if the Playable's current health value
      is above zero. subclasses that add stats bonuses must
      override this method.'''
      return self.getStats().getHealth().getCurrent() > 0
   
   # setters
   def equip(self, gear):
      '''equip passed gear and update the stats. return
      the old gear equipped at slot; or none if there
      was none.'''
      old = self.equipment.setGear(gear)
      return old
   
   # override tostring
   def __str__(self, short = True):
      descr = super().__str__(short)
      if not short:
         descr += '\n' + self.equipment.__str__()
      return descr

# Monster object
class Monster(Unit):
   '''a subclass of a Unit object. this represent a non-
   abstract monster which adds to units characteristics
   a development method that allows it to be spawned at
   any level desirable.'''
   
   def __init__(self, name: str, level: int, bStats: list,
      bSkill: Skill, lore: str, elt = NOELM):
      super().__init__(name, level, bStats, 3, bSkill, elt)
      self.lore = lore
      self.develup()
   
   # getters
   def getLore(self) -> str:
      '''return the lore surrounding this Monster.'''
      return self.lore
   
   # stats development
   def develup(self) -> bool:
      '''adjust the stats of the monster to match its
      level. basically, every stat is raised by its half 
      for every level after level 1. Luck is up to luck :)
      this is called in the monster constructor.
      '''
      newStats = self.stats.getFullStats()
      dev = [150, 150, 150, 150, 150, 150] 
      lvlGain = self.level.getCurrent() - 1
      for lvl in range(lvlGain): # for each new lvl
         # hp, ..., dext
         newStats = [ceil(newStats[idx] * dev[idx] / 100) \
            for idx in range(6)]
         # append luck to the list
         newStats.append(self.stats.getStat("luck").getFull())
         # luck increases by at most 3
         newStats[6] += rndGen(3)
      # assign new stats
      self.stats = UnitStats(newStats)
   
   # override tostring
   def __str__(self, short = True):
      '''return a string representing this object for
      printing purposes.'''
      description = super().__str__(short)
      if not short:
         description += "class <Monster>:"
         description += '\n' + self.lore
      return description

# BossMonster object
class BossMonster(list):
   '''a boss monster differs from normal monsters by
   the fact that they don't just get defeated once
   their hp reaches 0. they have multiple forms
   each giving them stats boosts. defeating them in
   all their form is required. this is the ultimate
   test of an adventurer's power.'''
   def __init__(self):
      self.current = 0
      
   # getters
   def getForms(self) -> int:
      '''return the number of forms of the boss.'''
      return len(self)
   def getNextForm(self) -> Monster:
      '''get the current form of the boss monster. update
      the current attribute to reflect what form to
      match the next getForm() call. this only works if
      current < len(self) else it returns None.'''
      form = None
      if self.current < len(self): # we have more forms
         form = self[self.current]
         self.current += 1   
      return form
   
   # setters
   def addForm(self, monster: Monster):
      '''adds a form to the boss monster.'''
      self.append(monster)
   
# test platform
if __name__ == "__main__":
   pass