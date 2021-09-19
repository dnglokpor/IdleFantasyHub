'''
# skills.py
# contains the declaration of the Skill and the SkillSet
# objects. a skill is any action that a unit can perform in 
# combat. in a combat round, units take turn performing
# skills. skills require a state that gives them the information
# they need to function. this class cannot be created this
# low in the OOP chain thus a base is provided here as a dub
# for the skills and will be overriden by the actual state
# object at a higher level.
# date: 6/25/21
# author: dnglokpor
# [U] 7/4/21: skills now contains the definition of the Mastery
# the Effect and the EffectList.
'''

# import
from base import Cooldown
from elements import Element, NOELM
import icecream as ice

dbg = ice.icecream.IceCreamDebugger()

# State base object
class State:
   '''a dub for BattleState created in confrontation.
   used to avoid circular dependency.'''
   def __init__(self):
      pass # do nothing

# Skill object
class Skill:
   '''a skill has a name, a description, a cooldown
   and an element. skills will in instance be subclasses
   of this base Skill class thus they must override the
   __call__ method.'''
   
   def __init__(self, name: str, descr: str, cd: int,
      elt = NOELM, power = 1.0):
      self.name = name
      self.description = descr
      self.cd = Cooldown(cd)
      self.element = elt
      self.power = power
   
   # getters
   def getName(self) -> str:
      '''return the skill name.'''
      return self.name
   def getElement(self) -> Element:
      '''return the Element of the skill.'''
      return self.element
   def getCD(self) -> Cooldown:
      '''return the skill CD object.'''
      return self.cd
   def getPower(self) -> float:
      '''return the power of the move.'''
   def isReady(self) -> bool:
      '''return "True" if the skill cooldown is elapsed.'''
      return self.cd.isCooled()
   
   # other
   def __eq__(self, other) -> True:
      '''overriden equality operator for skills. discriminate
      by name an CD and description.'''
      if other is None:
         return False
      else:
         return ((self.name == other.name) and
            (self.description == other.description) and
            (self.cd.getTime() == other.cd.getTime()))
   def __ne__(self, other) -> True:
      '''overriden unequality operator for skills. return
      the contraposition of "__eq__"'''
      return not self.__eq__(other)
   
   # makes the skill callable
   def __call__(self, state: State) -> tuple:
      '''execute the effect of the skill. since the skill
      occurs in battle, "state" refer to the current state
      of the battle as a whole which is used by the move
      to apply its effects. returns a a tuple containing
      all successfully hit opponents and a string describing
      the overall effect. this must be overriden by each
      skill subclasses.'''
      return (None, "nothing to see here.")
      
   
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = "{} <CD {}>:\n".format(self.name,
         self.cd.getTime())
      description += self.description
      return description

# SkillSet object
class SkillSet(dict):
   '''a unit can have up to 4 active skills forming a
   skill set. each skill has a specific purpose:
   - a base skill is the basic action a unit can perform
   in combat. the base skill has 0 of cooldown thus always
   available.
   - the ability skill is a special action that the unit
   can do when available in place of the base skill.
   - the reaction skill is a skill that will be performed
   when available but only as a reaction to an opponent
   skill targetting the unit.
   - a critical skill is a special skill that only gets
   called if in battle vitality drops under 20% of full
   health.
   this object provides a placeholder slots for the set.
   the base skill cannot be replaced.'''
   
   def __init__(self, bSkill: Skill):
      '''the base skill is set at construction.'''
      # create the underlying dict
      super().__init__({
         "base": bSkill, "ability": None, "reaction": None,
         "critical": None
      })
   
   # getters
   def getSkill(self, sKey) -> Skill:
      '''return the requested skill out of the skill set
      if the skill is defined. return None if the skill
      is not set or when not defined.'''
      if self.__contains__(sKey):
         return self.get(sKey)
      else: # skill not defined
         # print("defined skills are: {}".format(
         #    [s for s in self.keys()]))
         return None
   def getBestAction(self) -> Skill:
      '''return either the ability or the base skill
      depending or whether or not the ability is 
      ready.'''
      action = self.get("ability")
      if action == None or (not action.isReady()):
         # ability isn't available 
         action = self.get("base") # default to base
         
      return action
   
   # setters
   def assign(self, sKey : str, skill) -> bool:
      '''set the skill attributed to reaction
      or support. the base skill can't be changed.
      a same skill can't be assigned to two different
      slots. sKey must be one of the 3 possible key of
      the set. return True if assignment happened; False
      if not.'''
      done = False
      if self.__contains__(sKey) and sKey != "base":
         # search for skill already set elsewhere
         for k, sk in self.items():
            if sk == skill:
               # and unassign it
               self.__setitem__(k, None)
         self.__setitem__(sKey, skill) # assign it at new spot
         done = True
      return done
   def unassign(self, sKey: str):
      '''remove a skill from a slot.'''
      if self.__contains__(sKey):
         self.__setitem__(sKey, None)
   
   # others
   def tick(self):
      '''cools all skills of the skill set.'''
      for skill in self.values():
            if skill != None:
               skill.getCD().cool() # if skill isn't ready
   
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = str()
      for skill in self.items():
         description += "[{:8s}] -> ".format(skill[0])
         if skill[1] is not None:
            description += "<{} | CD: {}>\n".format(
               skill[1].getName(), skill[1].getCD().getTime())
         else:
            description += "not set\n"
      return description

# Mastery object
class Mastery(dict):
   '''the mastery is a collection of moves that are available
   for an adventurer as he gets stronger in a specific class.
   the key is the level at which the skill is available and
   the skill itself is the value.'''
   
   def __init__(self, name: str, lore: str, allSkills: list):
      '''"allSkills" must be a list of tuples.'''
      super().__init__(allSkills)
      self.name = name
      self.lore = lore
   
   # getters
   def getName(self) -> str:
      '''return the Mastery's name.'''
      return self.name
   def getName(self) -> str:
      '''return the Mastery's lore.'''
      return self.lore
   def getBase(self):
      '''the base skill is the skill added to the mastery with
      key "1". if not defined return "None".'''
      return self.get(1)
   def getSkill(self, uLevel: int, aLevel: int):
      '''return the skill corresponding at "uLevel" if
      "uLevel" is defined and if "uLevel <= aLevel".
      does not return the base skill.'''
      sk = None
      if self.__contains__(uLevel) and uLevel > 1:
         if uLevel <= aLevel:
            sk = self.get(uLevel)
      return sk
   def getUnlocked(self, currentLevel: int) -> list:
      '''return a list of all the skills that are
      already available at "currentLevel" except for
      the base skill.'''
      unlocked = list()
      for lvl, skill in self.items():
         if 1 < lvl <= currentLevel:
            unlocked.append(skill)
      return unlocked
   
   # Mastery is never set
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = "<{}>: {}".format(self.name, self.lore)
      if not short:
         description += '\n'
         for idx, (lvl, skill) in enumerate(self.items()):
            description += "{:12s} - unlocks @ lvl {:3d}".format(
               skill.getName(), lvl)
            if idx != len(self.items()) - 1:
               description += '\n'
      return description


INFINITY = 10000 # 10k turns is too long for any fight

# Effect object
class Effect:
   '''an Effect represent a lingering condition that
   impacts a character's stats. a unit can be affected
   by multiple effects at the time. just like a skill,
   an effect has a function as part of its member variables.
   an effect will expire once it's duration reaches "0".
   '''
   def __init__(self, dur: int, impacted: str, cond,
      power = 1.25):
      self.dur = dur
      self.impacted = impacted
      self.condition = cond # function that
      self.power = power
   
   # getters
   def isExpired(self):
      '''return "True" if the effect has reached 
      the end of its countdown.'''
      return self.dur == 0
   
   # setters
   def countDown(self):
      '''decrease effect duration by a unit.'''
      if self.dur != 0:
         self.dur -= 1
   
   # others
   def __eq__(self, other) -> True:
      '''overriden equality operator for effects. discriminate
      by duration an condition and impacted.'''
      if other is None:
         return False
      else:
         return ((self.dur == other.dur) and
            (self.condition == other.condition) and
            (self.impacted == other.impacted))
   def __ne__(self, other) -> True:
      '''overriden unequality operator for effects. return
      the contraposition of "__eq__"'''
      return not self.__eq__(other)
   
   # makes this callable to apply the condition
   def __call__(self, unit) -> str:
      '''apply self.condition to the unit. return the amount
      by which the effect impacted the stats.'''
      return self.condition(unit, self.impacted, self.power)

# EffectList object
class EffectList(list):
   '''a unit can be affect by more than one effect at
   the time thus this object keeps track of them all.'''
   
   def __init__(self):
      super().__init__() # empty list
   
   # getters 
   def isEmpty(self):
      '''return "True" is the EffectList is empty.'''
      return len(self) == 0
   
   # setters
   def addEffect(self, ef: Effect):
      '''add a new effect to the list of effects.'''
      self.append(ef)
   def tick(self):
      '''traverse the list and trigger the countdown
      method of all the effects.'''
      for effect in self:
         effect.countDown()
   def removeExpired(self):
      '''clear any Effect from the list that is expired.'''
      for effect in self:
         if effect.isExpired():
            self.remove(effect)   
  
   # others
   def applyAll(self, unit):
      '''apply all still active effects'''
      self.removeExpired() # remove expired
      for e in self:
         # apply the effects
         e(unit)   
   
# test platform
if __name__ == "__main__":
   pass
   