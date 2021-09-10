'''
# base.py
# module that contains the definition of all base classes
# of objects created for IdleFantasyHub world such as
# Stat, Gauge, Skill etc...
# date: 6/25/21
# author: dnglokpor
'''

# Stat object
class Stat(dict):
   '''subclass of dict that define a collection of values
   that represent the full and current values of a unit
   combat attribute.'''
   def __init__(self, full = 0, current = None):
      # create base dict
      if current == None:
         current = full
      super().__init__({"full": full, "current": current})
      
   # getters
   def getFull(self) -> int:
      '''return the full value of the stat.'''
      return self.get("full")
   def getCurrent(self) -> int:
      '''return the current value of the stat.'''
      return self.get("current")
    
   # setters
   def reset(self):
      '''return current to full value.'''
      self.__setitem__("current", self.get("full"))
   def setFull(self, val: int):
      '''set the full value of the stat to "val". "val"
      must be positive (>= 0).'''
      if 0 <= val:
         self.__setitem__("full", val)
   def setCurrent(self, val: int):
      '''set the current value of the stat to "val". "val"
      must be positive (>= 0).'''
      if val >= 0:
         self.__setitem__("current", val)

   # overload addition operator
   def __add__(self, other) -> dict:
      '''adds this Stat object to another one by value:
      full added to full and current added to current.
      return a new Stat object.'''
      result = Stat() # new stat with zero
      result.setCurrent(self.getCurrent() +
         other.getCurrent())
      result.setFull(self.getFull() +
         other.getFull())
      return result
   
   # override tostring
   def __str__(self, ratio = False) -> str:
      '''return a string representing this object for
      printing purposes. ratio can be set to true
      to get the print out in the form of the ratio
      of the current value over the full value.'''
      if ratio:
         return "{:3d}/{:3d}".format(self.getCurrent(),
            self.getFull())
      else:
         return "{:7d}".format(self.getCurrent())

# possible stats list
STATS = ["health", "attack", "defense", "special", 
   "resilience", "dexterity", "luck"]

# UnitStats class
class UnitStats(dict):
   '''a unit needs a collection of attributes for combat
   purposes called stats: the health stat for durability,
   the attack stat for offense, the defense stat for 
   resilience, the dexterity stat for movement speed and
   evasion and the luck stat for fortune. this class
   represent that collection of these stats and methods
   to modify them. this collection is based on python
   lists thus it can be treated as such.'''
   
   def __init__(self, stats: list):
      '''expect the full value of each 7 stat. each
      current value will be set to the same as the full
      value.'''
      if len(stats) != 7:
         raise ValueError
      super().__init__({
         STATS[0]: Stat(stats[0], stats[0]), # hp
         STATS[1]: Stat(stats[1], stats[1]), # atk
         STATS[2]: Stat(stats[2], stats[2]), # def
         STATS[3]: Stat(stats[3], stats[3]), # spe
         STATS[4]: Stat(stats[4], stats[4]), # res
         STATS[5]: Stat(stats[5], stats[5]), # dext
         STATS[6]: Stat(stats[6], stats[6])  # luck
      })
   
   # getters
   def getHealth(self) -> Stat:
      '''return the health stat.'''
      return self.get(STATS[0])
   def getStat(self, sName: str) -> Stat:
      '''return the stat associated with "sName". if sName
      is invalid, default to health.'''
      if self.__contains__(sName):
         return self.get(sName)
      else:
         self.getHealth()
   def getFullStats(self) -> list:
      '''return a list of the full values of all stats.'''
      return [self.getStat(STATS[0]).getFull(),
         self.getStat(STATS[1]).getFull(),
         self.getStat(STATS[2]).getFull(),
         self.getStat(STATS[3]).getFull(),
         self.getStat(STATS[4]).getFull(),
         self.getStat(STATS[5]).getFull(),
         self.getStat(STATS[6]).getFull()
      ]
   
   # setters
   def setStat(self, sName: str, val: int):
      '''set current value of the stat to "val".
      current health will have an extra test to not go
      over its full value.'''
      if self.__contains__(sName): # can only set existing stat
         if val < 0: # val must be positive
            val = -val
         if (sName == STATS[0] and 
            val > self.getHealth().getFull()):
            # case of health so we go up to full health
            val = self.getHealth().getFull()
         self.getStat(sName).setCurrent(val) # set it
   def changeBy(self, sName: str, dmg: int):
      '''set current value of a stat to its previous value
      added to "dmg". dmg is negative when its a loss,
      positive when its a gain.'''
      old = self.getStat(sName).getCurrent()
      new = old + dmg
      if new < 0:
         new = 0
      self.setStat(sName, new)
   def cleanse(self):
      '''remove any change in stats except for hp.'''
      for key, stat in self.items():
         if key != STATS[0]:
            stat.reset()
   
   # overload addition operator
   def __add__(self, other) -> dict:
      '''provide a way to add two UnitStats objects
      together. the resulting object is a UnitStats
      object with full values and current values that
      are the full and current values of the unit and
      the equipment.'''
      result = UnitStats([0, 0, 0, 0, 0, 0, 0])
      for sName, sObj in self.items():
         result.__setitem__(sName,
            self.getStat(sName) + other.getStat(sName)
         )
      return result   
   
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = str()
      for key, stat in self.items():
         if key == STATS[0]: # health should be a ratio
            description += "{:10s}: {}".format(key, 
               stat.__str__(True))
         else:
            description += "{:10s}: {}".format(key, 
               stat.__str__())
         if key != STATS[6]:
            description += '\n'
      return description

# Gauge object
class Gauge:
   '''a gauge is a counter that keeps track of a current
   value that increases to a treshold, increment a level
   and reset itself until it reaches a limit. this object
   provides the attributes of a basic finite gauge and 
   management methods.'''
   
   def __init__(self, lvl = 1, lim = 99):
      '''creates a new gauge with optionally the current
      level of the gauge. other attributes depend on that
      current level. the default limit is 99.'''
      self.level = lvl
      self.current = 0
      self.treshold = self.level * 100
      self.lim = lim
   
   # getters:
   def getCurrent(self):
      '''get the current level of the gauge.'''
      return self.level
   
   # setters
   def updateTreshold(self):
      '''adapt the treshold to the current level.'''
      self.treshold = self.level * 100

   def levelup(self, gain) -> tuple:
      '''increase current by "gain". update level and
      thresholds if necessary. "gain" must be absolutely
      positive (> 0) and level can only go as high as 
      "self.lim". return a tuple that says if a level
      up happened and by how many levels.'''
      lvlUp = False
      count = 0
      if gain > 0: # gain absolutely positive
         if self.level <= self.lim: # can't level up after limit
            while gain > 0:
               need = self.treshold - self.current
               if need > gain:   # not enough to level up
                  self.current += gain # increase current
                  gain = 0             # we used it up
               else:             # enough to levelup
                  gain -= need      # use up needed gain
                  self.level += 1   # lvl up
                  lvlUp = True      # flag lvl up
                  count += 1
                  self.current = 0  # reset current
                  self.updateTreshold()
      
      return (lvlUp, count)
               
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      descr = "LVL {:3d}".format(self.level)
      if not short:
         descr += " (exp. {:4d}/{:4d})".format(self.current, 
            self.treshold)
      return descr

# CD object
class Cooldown:
   '''a cooldown is the property of something that can
   be used only once in a while. when unavailable, its
   in cooldown. this object will track the state of the
   availability and reset the cooldown as needed.'''
   
   def __init__(self, length: int):
      '''the thing in cooldown will only be available
      once every "length" occurence of the unit duration.'''
      self.cdTime = length
      self.currentCD = 0
   
   # getters
   def getTime(self):
      '''return the cooldown time.'''
      return self.cdTime
   def getElapsed(self):
      '''return the cooldown current value.'''
      return self.currentCD
   def isCooled(self):
      '''return "True" when the cooldown duration has been
      reached. else "False".'''
      return self.currentCD == self.cdTime
   
   # setters
   def reset(self):
      '''reinitialize the current value of the CD.'''
      self.currentCD = 0
   def cool(self):
      '''increase the current value of cooldown by a unit
      if the current is not less than "self.cdTime".'''
      if self.currentCD < self.cdTime:
         self.currentCD += 1
         
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes.'''
      return "CD {:2d} out of {:2d}".format(self.currentCD,
         self.cdTime)
   
   
# test platform
if __name__ == "__main__":
   pass
   