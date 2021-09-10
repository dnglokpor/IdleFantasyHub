'''
# unit.py
# module that contains all the classes needed to create
# a virtual IdleFantasyHub unit. contains the definition
# of the UnitStats, Unit, and Playable.
# date: 6/25/21
# author: dnglokpor
'''

# imports
from base import Stat, STATS, UnitStats
from base import Gauge
from elements import Element, NOELM
from skills import Skill, SkillSet, EffectList
from collectibles import Item, Equipment
from containers import Inventory, Wallet

# Unit object
class Unit:
   '''units are abstract base mobs of IdleFantasyHub.
   only units can participate in combat. this class
   provides what is needed to identify and represent
   a unit.'''
   
   def __init__(self, name: str, level: int, stats: list, 
      bSize: int, elt = NOELM):
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
      elt = NOELM):
      # create underlying Unit
      super().__init__(name, level, stats, 30, elt)
      self.equipment = Equipment()
      self.wallet = Wallet()     # empty wallet
   
   # getters
   def getEquipped(self) -> Equipment:
      '''get the Equipment attribute of the Playable.'''
      return self.equipment
   def getWallet(self) -> Wallet:
      '''return the Wallet attribute of the Playable.'''
      return self.wallet
   def getStats(self) -> UnitStats:
      '''return the combinedStats attribute of the Playable.
      overrides the getStats() method of the super Unit
      class.'''
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

# test platform
if __name__ == "__main__":
   pass