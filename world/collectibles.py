'''
# colletibles.py
# this module defines objects that can be collected meaning
# stored in the player's storage. such objects will be based
# on the Item class but the collectibles can be instances of
# subclasses of Item: Gear and its 3 variants. to model the
# triplet weapon, armor and accessory that playable units
# can equip is the purpose of the Equipment object.
# date: 6/27/21
# author: dnglokpor
'''

# imports
from base import Stat, STATS

# helper
def genHash(name) -> str:
   '''return an integer that is a deterministic result
   of computing a "name" string through this algorithm.
   '''
   base = 100001 # prime
   name = name.lower() # case non-sensitive
   gen = ord(name[0])
   for c in name[1:]:
      gen *= ord(c)
   return (gen // base) + (gen % base)
   

# Item object
class Item:
   '''anything that can be collected is an object. this
   basic class provides fields for an item hash, name,
   lore, and value (in the IdleFantasyHub value system).'''
   
   def __init__(self, name: str, lore: str, value: int):
      '''builds and object using provided name, a description
      and its value. the hash is a unique ID based on the name
      and value.'''
      if len(name) == 0 or len(lore) == 0:
         raise ValueError("name and lore cannot be empty\
strings")
      if value < 0:
         raise ValueError("value must be positive (>= 0)")
      self.name = name
      self.lore = lore
      self.value = value
      self.ID = genHash(self.name)
   
   # getters
   def getID(self) -> int:
      '''return the unique ID associated with this item.'''
      return self.ID
   def getName(self) -> str:
      '''return the name of the item.'''
      return self.name
   def getValue(self, selling = False) -> int:
      '''return the value of the object. the selling flag
      does the calculations for selling items which returns
      only half the value.'''
      if not selling:
         return self.value
      else:
         return self.value // 2
   
   # item attributes are never set
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      descr = "{:15s} (value: {:5d})".format(self.name,
         self.value)
      if not short:
         descr += "\n{}".format(self.lore)
      return descr

# Gear object
class Gear(Item):
   '''a gear item is different from a regular item by the
   fact that it has a list of stats. these improve the same
   stats on the unit who wears them.'''
   
   def __init__(self, name: str, lore: str, value: int,
      stats: list):
      '''a stat here is represented by the tuple 
      (name, value). stats can't be empty.'''
      if len(stats) == 0:
         raise ValueError("no stats were provided.")
      super().__init__(name, lore, value)
      self.stats = stats
   
   # getters
   def getStats(self) -> list:
      '''return the stats list.'''
      return self.stats
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = super().__str__(short) + '\n'
      for idx, (name, value) in enumerate(self.stats):
         op = '+'
         if value < 0:
            op = '-'
         description += "{}{}{}".format(name[:3], op, abs(value))
         if idx != len(self.stats) - 1:
            description += ', '
      
      return description
      
# Gear variants
# Weapons
class Weapon(Gear):
   '''a weapon is a gear that generally improves offensive
   stats.'''
   
   def __init__(self, name, lore, value, stats):
      super().__init__(name, lore, value, stats)
      self.t = "WPN"
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      return "[{:3s}]".format(self.t) + super().__str__(short)

# Sword
class Sword(Weapon):
   '''a sword shaped weapon. derivation allows to filter
   it out of all weapons.'''
   
   def __init__(self, name, lore, value, stats):
      '''only inits the base Weapon.'''
      super().__init__(name, lore, value, stats)

# Sword
class Spear(Weapon):
   '''a sharp combat spear. derivation allows to filter
   it out of all weapons.'''
   
   def __init__(self, name, lore, value, stats):
      '''only inits the base Weapon.'''
      super().__init__(name, lore, value, stats)

# Bow
class Bow(Weapon):
   '''a stringy bow - arrows non included. derivation 
   allows to filter it out of all weapons.'''
   
   def __init__(self, name, lore, value, stats):
      '''only inits the base Weapon.'''
      super().__init__(name, lore, value, stats)

# Artillery
class Artillery(Weapon):
   '''a high level ranged weapon. derivation allows to
   filter it out of all weapons.'''
   
   def __init__(self, name, lore, value, stats):
      '''only inits the base Weapon.'''
      super().__init__(name, lore, value, stats)

# Staff
class Staff(Weapon):
   '''a wand that help with magic conjunction. derivation
   allows to filter it out of all weapons.'''
   
   def __init__(self, name, lore, value, stats):
      '''only inits the base Weapon.'''
      super().__init__(name, lore, value, stats)

# Tome
class Tome(Weapon):
   '''a magic caster preferred weapon. derivation allows
   to filter it out of all weapons.'''
   
   def __init__(self, name, lore, value, stats):
      '''only inits the base Weapon.'''
      super().__init__(name, lore, value, stats)

# Armor
class Armor(Gear):
   '''armor is gear that improve your resistance to harm.'''
   
   def __init__(self, name, lore, value, stats):
      super().__init__(name, lore, value, stats)
      self.t = "ARM"
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      return "[{:3s}]".format(self.t) + super().__str__(short)

# Accessory
class Accessory(Gear):
   '''an accessory is a gear is an extra piece of gear that
   provides stats bonuses.'''
   
   def __init__(self, name, lore, value, stats):
      super().__init__(name, lore, value, stats)
      self.t = "ACC"
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      return "[{:3s}]".format(self.t) + super().__str__(short)

# all Equipment slots:
SLOTS = ["WPN", "ARM", "ACC"]

# Equipment object
class Equipment(dict):
   '''the collection of the 3 gear that an playable can
   have at the time. based off a dict for convenience.'''
   
   def __init__(self):
      '''construction requires no actual gear. defines
      placeholders for them.'''
      super().__init__({"WPN": None, "ARM": None, "ACC": None})
  
   # getters
   def getGear(self, slot: str):
      '''return the requested gear out of the Equipment.
      if nothing was equiped there, return "None".'''
      g = None
      if(self.__contains__(slot)):
         g = self.get(slot)
      return g
   
   def getEqtBonus(self) -> list:
      '''returns as a list formated in the order of the 
      base.STATS the combined stats bonuses (or maluses)
      conferred by the equipment pieces.'''
      comb = [0, 0, 0, 0, 0]
      for g in self.values():
         if g != None: # not empty slot
            for sName, val in g.getStats():
               comb[STATS.index(sName)] += val
      return comb
   
   # setters
   def setGear(self, gear: Gear) -> Gear:
      '''assign passed gear to the right slot. this depends
      on the existence of the "t" attribute of passed
      gear thus if gear doesn't have it, ValueError is
      raised. returns the old gear set at the slot if any
      or just None.'''
      old = None
      slot = None
      try:
         slot = gear.t
      except AttributeError: # gear without a "t" attribute
         raise ValueError("passed gear is not a Weapon, Armor\
or Accessory type object.")
      old = self.get(slot)
      self.__setitem__(slot, gear)
      return old         
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = str()
      for t, gear in self.items():
         description += "[{}] -> ".format(t)
         if gear is not None:
            description += "<{}>\n".format(gear.getName())
         else:
            description += "not set\n"
      return description

# test platform
if __name__ == "__main__":
   #beastFur = Item("Beast Fur", 
   #   "freshly skinned fur of a denizen of the woods.",
   #   5
   #)
   #print(beastFur.__str__(False))
   #print("its ID is: {}".format(beastFur.getID()))
   
   gladius = Weapon("Gladius", 
      "an arm-long glaive in made of heavy iron.",
      250, [(STATS[1], 30), (STATS[3], -5)]
   )
   #print(gladius.__str__(False))
   cuirrass = Armor("Cuirrass", 
      "a small plastron made of leather interwoven on a tin frame.",
      110, [(STATS[2], 15)]
   )
   #print(cuirrass.__str__(False))
   silverLocket = Accessory("Silver Locket", 
      "a locket that is said to ward off werewolves.",
      300, [(STATS[3], 3), (STATS[4], 2)]
   )
   #print(silverLocket.__str__(False))
   me = Equipment()
   print(me)
   me.setGear(cuirrass)
   #me.setGear(gladius)
   me.setGear(silverLocket)
   print(me)
   print("combined equipment bonus is: ", me.getEqtBonus())