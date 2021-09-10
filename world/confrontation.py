'''
# confrontation.py
# this module defines the required objects and methods
# to moderate combat in IdleFantasyHub. the idea here is
# that a battle can be at each iteration defined by a 
# BattleState: the combination of the two opposing parties,
# a TurnOrder object, a status flag and a round counter.
# when a battle start, two parties are assigned. units of
# each parties are allowed to move in a turn-base action
# system based on their dexterity stat (highest dext moves
# first). a round is defined as the turn order until all
# the units have moved at least once. the battle ends when
# any of the parties dies thus setting the status flag.
# the Battle object uses information of the BattleState
# object to run through a full battle and designate the
# the victorious party (award exp?).
# date: 7/1/21
# author: dnglokpor
'''

# imports
from base import STATS
from time import sleep
from copy import deepcopy
from math import ceil
from math import exp as E
from random import choice
from sys import exit
try:
   from units import Playable
except ImportError:
   print("Couldn't import playable")
   exit()
from icecream import IceCreamDebugger

# DEBUG
dbg = IceCreamDebugger()

# helpers
def getHP(unit):
   return unit.getStats().getHealth().getCurrent()

# Party object
class Party(list):
   '''a party is a group of units that are on the same
   side in combat situation. they consider each other
   allies. this object allows to track them and their
   status more easily.'''
   
   def __init__(self, unitsList: list):
      # create the party from the regular list
      super().__init__(unitsList)
      # add affixes to repeated names
      if len(self) > 1:
         for i, unit in enumerate(self):
            count = 0
            name = unit.getName()
            for idx in range(i+1, len(self)):
               if self[idx].getName() == name:
                  count += 1
                  self[idx].addLetter(count)
   
   # getters
   def getSize(self) -> int:
      '''return the size of the party.'''
      return len(self)
   def getMember(self, unitOrder):
      '''return one unit of the party. "unitOrder" must
      be an integer between 0 and the size of the party
      exclusive.'''
      if unitOrder >= self.getSize():
         raise IndexError("party doesn't have that many\
 members.")
      return self.__getitem__(unitOrder)
   def getWeakestMember(self):
      '''return the member of the party that has the
      lowest current health stat if applicable.'''
      # make a copy list
      copy = [u for u in self]
      # sort in ascending order
      copy.sort(key = getHP)
      # find unit alive with lowest HP
      idx = 0
      while idx < len(copy) and not copy[idx].isAlive():
         idx += 1
      # current copy[idx] unit is weakest
      return copy[idx]
   def getMembers(self) -> list:
      '''return all the units members of the party as a
      simple python list variable.'''
      return list(self)
   def stillStands(self) -> bool:
      '''return "True" if any of the units of the Party
      are still alive (a.k.a has HP > 0).'''
      idx = 0
      alive = False
      while idx < self.getSize() and not alive:
         alive = self.__getitem__(idx).isAlive()
         if not alive:
            idx += 1
      return alive
   
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = str()
      for unit in self:
         description += '<' + unit.__str__()
         description += " |HP: "
         description += unit.getStats().getHealth().__str__(True)
         description += '>'
         if unit != self.__getitem__(-1): # not last
            description += '\t'
      return description

# TurnOrder object
class TurnOrder:
   '''a round stops only when all units in the battle have
   moved once. this object tracks each units and creates 
   an iterable list that returns the next to move, keeing
   it updated.'''
   
   def __init__(self, allUnits: list):
      '''create the attributes of the turn order object
      by receiving a list of all the units in battle.'''
      self.units = allUnits
   
   # getters
   # iterator override
   # this object will now be iterable and the next() method
   # will return the next character that moves until none
   # can move anymore i.e. their speed < 0.
   def __iter__(self):
      '''setup the iterator for the TurnOrder object.'''
      # create an image of the current stats to
      # track dexts in case one changes.
      self.oDexts = list()
      for u in self.units:
         self.oDexts.append(
            u.getStats().getStat(STATS[5]).getCurrent()
         )
      # create a table that relate each unit to their dext
      self.mutDexts = [(self.units[i], self.oDexts[i])\
         for i in range(len(self.units))]
      self.mutDexts = dict(self.mutDexts)
      # create a field for round the lowest dext
      self.lowDext = min(self.oDexts)
      return self
   def __next__(self):
      '''return the unit of this TurnOrder that moves
      next by doing arithmetic on their dexterity.'''
      # compare recorded dexterities with currents
      for idx in range(len(self.oDexts)):
         u = self.units[idx]
         nDext = u.getStats().getStat(STATS[5]).\
            getCurrent()
         oDext = self.oDexts[idx]
         if nDext != oDext: # dext changed
            # take the algebraic difference
            diff = nDext - oDext
            # find the unit and apply same diff
            old = self.mutDexts[u]
            self.mutDexts.__setitem__(u, old + diff)
            # updtate entry
            self.oDexts[idx] = nDext
      # dext updates are completed
      # checks for dead units
      for u, d in self.mutDexts.items():
         if not u.isAlive():
            # kick them out of the turn
            self.mutDexts.__setitem__(u, -1)
      # look for fastest unit and its current dext
      maxDext = 0
      fastest = self.units[maxDext]
      for u, d in self.mutDexts.items():
         if d > maxDext:
            maxDext = d
            fastest = u
      # compare fastest dext to standard dext
      if maxDext < self.lowDext: # round over then
         raise StopIteration
      # else implied: fastest moves next
      # reduce their dext according to standard dext
      self.mutDexts.__setitem__(fastest, maxDext - self.lowDext)
      # return them
      return fastest
   
   # override tostring
   def __str__(self):
      string = "Turn Order: "
      for u in self:
         string += "{}| ".format(u.getName())
      return string

# BattleState object:
class BattleState:
   '''class that compiles all information relative
   to the state of a battle in one object. this allows
   any party involved to be able to know all there
   is to know in the battle at all time.'''
   
   def __init__(self, pro: Party, cons: Party):
      '''create the state by getting the two opposing
      parties and initializing all other member variables.
      '''
      self.pro = pro
      self.cons = cons
      self.turnOrder = TurnOrder(self.pro.getMembers() +
         self.cons.getMembers())
      self.moving = None # field to record whose turn it is
      self.waste = list() # stores lost items during battle
   
   # getters
   def getAllies(self, unit) -> Party:
      '''return the party that "unit" is part of.'''
      party = self.pro
      try:
         party.index(unit)
      except ValueError: # was not in that party
         party = self.cons
      return party
   def getOpponents(self, unit) -> Party:
      '''return the party that "unit" is NOT part of.'''
      party = self.getAllies(unit)
      if party == self.pro:
         party = self.cons
      else: # party == self.cons
         party = self.pro
      return party
   def getTurnOrder(self) -> TurnOrder:
      '''return the turn order object of the BattleState.'''
      return self.turnOrder
   def isMoving(self):
      '''return the unit currently moving.'''
      return self.moving
   def getWaste(self):
      return self.waste
   def isOver(self):
      '''return "True" if any of the two parties involved
      has been defeated.'''
      return ((not self.pro.stillStands()) or 
         (not self.cons.stillStands()))
   
   # setter
   def addLostItem(self, owner, item):
      '''add an item to the waste list.'''
      self.waste.append((owner, item))
   
   # battle method
   def run(self, verbose = True):
      '''runs a battle between the two parties involved in
      the encounter. a battle only stops if one party has
      been defeated meaning they have no more members
      standing. the "verbose" flag allow for console print.'''
      roundNo = 0
      print("a battle has started:\n") # DEBUG
      sleep(1)                         # DEBUG 
      while not self.isOver(): # battle loop
         print(self)                   # DEBUG
         print("Round ", roundNo + 1)  # DEBUG
         sleep(3)                      # DEBUG
         for unit in self.turnOrder: # round loop
            # update battle state
            self.moving = unit
            # cool skills
            unit.getSkillSet().tick()
            # apply effects
            unit.stats.cleanse() # base stats only
            unit.getActiveEffects().applyAll(unit)
            # action
            a = unit.getSkillSet().getBestAction()
            print("{} attempts {}!".format(unit.getName(),
               a.getName()))           # DEBUG
            sleep(2)                   # DEBUG
            result = a(unit, self)
            if type(result) != list:
               result = [result,] # convert to list
            # DEBUG BLOC
            for t, msg in result:
               print(msg)
               sleep(2)
            # END OF DEBUG BLOC
            # critical actions or reactions
            for t, msg in result:
               if t != None and t.isAlive():
                  c = t.getSkillSet().getSkill("critical")
                  r = t.getSkillSet().getSkill("reaction")
                  res = None
                  if (t.isCritical() and c!= None and 
                     c.isReady()):
                     # critical reaction branch
                     print("desperate, {} attempts {}!".format(
                        t.getName(), c.getName()))  # DEBUG
                     sleep(2)             # DEBUG
                     res = c(t, self)
                  elif r != None and r.isReady():
                     # reaction branch
                     print("{} attempts {} in return!".format(
                        t.getName(), r.getName()))  # DEBUG
                     sleep(2)             # DEBUG
                     res = r(t, self)
                  # else is implied
                  # DEBUG BLOC
                  if res != None:
                     print(res[1])
                     sleep(2)
                  # END OF DEBUG BLOC
            unit.getActiveEffects().tick() # countdown effects
            # check for end of battle
            if self.isOver():
               break
         # end of round loop
         if not self.isOver():
            roundNo += 1
            print("\n\n\n")            # DEBUG
      # end of battle loop
      winner = self.pro
      wName = "pro"
      if not self.pro.stillStands():
         winner = self.cons
         wName = "cons"
      print("{} won the battle!".format(wName)) # DEBUG
      return winner # return winning party         
   
   # post battle stuff
   def awardExp(self):
      '''make adventurers gain experience from their fight.'''
      allUnits = self.pro.getMembers()
      allUnits.extend(self.cons.getMembers())
      for u in allUnits:
         if isinstance(u, Playable):
            if u.isAlive():
               uLvl = u.getLevel().getCurrent()
               gain = 0
               for opp in self.getOpponents(u):
                  oLvl = opp.getLevel().getCurrent()
                  gain += (10 * ceil(E(oLvl - uLvl)))
               print("{} gained {} exp. pts!".format(
                  u.getName(), gain)) 
               if u.develup(gain): # leveled up
                  print("{} has leveled up.".format(
                     u.getName()))
                  print(u.getStats().__str__(False))
   def collectLoot(self):
      '''allows adventurers to collect loot from monsters.'''
      mns = None
      adv = None
      if isinstance(self.cons.getMember(0), Playable):
         mns = self.pro
         adv = self.cons
      else:
         mns = self.cons
         adv = self.pro
      if mns != None and adv != None: # we have a vs case
         for m in mns:
            chances = 90
            for item in m.getBag():
               if choice(range(100)) <= chances:
                  for a in adv:
                     print("{} got {} from {}!".format(
                        a.getName(), item.getName(), 
                        m.getName()))
                     sleep(2)
                     a.getBag().add(item)
               chances -= 10 # reduces chances of getting next
   def recoverLostItems(self):
      '''a chance of recovering wasted items.'''
      for o, i in self.waste:
         chances = 90
         if choice(range(100)) <= chances:
            o.getBag().add(i)
            print("{} recovered {} x1".format(
               o.getName(), i.getName()))
            sleep(2)
         chances -= 5
         
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = self.pro.__str__()
      description += "\n\n\n"
      description += self.cons.__str__()
      description += '\n'
      description += self.turnOrder.__str__()
      return description

# test platform
if __name__ == "__main__":
   pass