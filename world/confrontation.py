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
from units import Unit

# testing imports
from skills import Skill
from units import Playable
from collectibles import Weapon, Armor, Accessory

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
   def getMember(self, unitOrder) -> Unit:
      '''return one unit of the party. "unitOrder" must
      be an integer between 0 and the size of the party
      exclusive.'''
      if unitOrder >= self.getSize():
         raise IndexError("party doesn't have that many\
 members.")
      return self.__getitem__(unitOrder)
   def getWeakestMember(self) -> Unit:
      '''return the member of the party that has the
      lowest level, or the lowest current health stat.
      if none of these conditions is met, return the
      first member of the party.'''
      weakest = None
      lvls = list
      for unit in self:
         if unit.isAlive():
            lvls.append(unit.getLevel().getCurrent())
      rLvls = lvls.reverse()
      lvl = min(lvls)
      if lvls.index(lvl) != rLvls.index(lvl):
         # there are more than one lowest level.
         hps = list
         for unit in self:
            if unit.isAlive():
               hps.append(unit.getStats().getHealth().getCurrent)
         hp = min(hps)
         weakest = self.__getitem__(hps.index(hp))
      else: # we found the lowest level
         weakest = self.__getitem__(lvls.index(lvl))
      return weakest
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
   moved once. this object tracks each units and creates a
   list that is their turn orders until the end of a round
   meaning until they have all moved once.'''
   
   def __init__(self, allUnits: list):
      '''create the attributes of the turn order object
      by receiving a list of all the units in battle.'''
      self.allUnits = allUnits
      self.movementTracker = list()
      for i in range(len(self.allUnits)):
         self.movementTracker.append(False)
   
   # getters
   def allHaveMoved(self) -> bool:
      '''return "True" when all the values in the
      movement tracker list are "True".'''
      count = 0
      for val in self.movementTracker:
         if val:
            count += 1
      return count == len(self.movementTracker)
   def getAllMoves(self) -> list:
      '''return the list that describes what order each
      of the units of the battle will move. this list
      is created by comparing the dexterity stat of
      each units. the slowest unit define the standard
      movement speed. fastest units will move first and
      they will move as much as the quotient of their
      dext to the standard dext.'''
      dextTracker = list()
      # record initial dexterities
      for unit in self.allUnits:
         dextTracker.append(unit.getStats()\
            .getStat(STATS[3]).getCurrent())
      standard = min(dextTracker) # slowest dext is standard
      # create turn order list
      turnOrder = list()
      # appends units to it
      while not self.allHaveMoved():
         # get index of fastest
         idx = dextTracker.index(max(dextTracker))
         # add fastest unit
         turnOrder.append(self.allUnits[idx])
         # mark that this unit has moved
         self.movementTracker[idx] = True
         # slow down by standard
         dextTracker[idx] -= standard
      return turnOrder
   
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes. calls self.getAllMoves() and
      return the next 5 moves or less if there isn't
      enough.'''
      description = "Moves Next: "
      moves = self.getAllMoves()
      done = False
      idx = 0
      count = 0
      while not done:
         try:
            description += "{} - {}| ".format(count + 1,
               moves[idx].getName())
            count += 1
            done = count == 5
            idx += 1
         except IndexError: # out of range
            done = True
      # done adding the names next 5 movers
      return description   

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
      self.effectList = list() # empty by default
   
   # getters
   def getAllies(self, unit: Unit) -> Party:
      '''return the party that "unit" is part of.'''
      party = self.pro
      try:
         party.index(unit)
      except ValueError: # was not in that party
         party = self.cons
      return party
   def getOpponents(self, unit: Unit) -> Party:
      '''return the party that "unit" is NOT part of.'''
      party = self.getAllies(unit)
      if party == self.pro:
         party = self.cons
      # no need of else as it is implied
      return party
   def getTurnOrder(self) -> TurnOrder:
      '''return the turn order object of the BattleState.'''
      return self.turnOrder
   def isOver(self):
      '''return "True" if any of the two parties involved
      has been defeated.'''
      return ((not self.pro.stillStands()) and 
         (not self.cons.stillStands()))
         
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

# battle method
def encounter(pro: Party, cons: Party, verbose = True):
   '''runs a battle between the two parties involved in
   the encounter. a battle only stops if one party has
   been defeated meaning they have no more members
   standing. the "verbose" flag allow for console print.'''
   bState = BattleState(pro, cons)
   roundNo = 0
   while not bState.isOver(): # battle loop
      roundNo += 1
      moves = bState.getTurnOrder.getAllMoves()
      idx = 0 # stays 0 all the way through
      while idx < len(moves) and (not bState.isOver()): # round loop
         # choose moving unit
         unit = moves[idx]
         # beginning of unit's turn
         # apply effects
         unit.getStats.cleanse() # reinit all stats
         unit.getActiveEffects().tick() # countdown
         unit.getActiveEffects().removeExpired()
         unit.getActiveEffects().applyAll() # update stats
         # cool all skills and use available
         unit.getSkillSet().coolAll()
         action = unit.getSkillSet().getBestAction()
         # execute action and put it in cooldown
         targets = action(unit, bState, None) # no oppressor
         action.getCD().reset()
         # check for reactions
         for victim in targets:
            react = victim.getSkillSet().getSkill("reaction")
            crit = victim.getSkillSet().getSkill("critical")
            if crit != None and crit.isReady():
               # critical reaction has priority
               crit(victim, bState, unit)
            elif react != None and react.isReady():
               # no critical reaction thus spontaneous reaction
               react(victim, bState, unit)
         # end of unit's turn
         moves.pop(idx) # pop that unit off the stack
   # end of battle loop
   winner = pro
   if not pro.stillStands():
      winner = cons
   return cons # return winning party


# test platform
if __name__ == "__main__":
   # TBD try a battle