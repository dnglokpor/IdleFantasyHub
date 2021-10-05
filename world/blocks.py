'''
# blocks.py
# blocks are the smallest units of the dungeon. they make
# up floors and are the meat of what the adventurers must
# explore. there are multiple type of blocks; each with
# specific events taking place in their environment.
# this module defines the Environment object as well as the
# Block base object and all the subvariations that can exist.
# date: 9/20/21
# author: dnglokpor
'''

# imports
from helpers import rndGen
from confrontation import Party, BattleState
import random as rnd

# Environment object
class Environment(dict):
   '''contains information about what the the inside of a
   block looks like as well as all the resources available
   in it. this information is stored as a dict with multiple
   fields:
    - the "look" is a list of sentences describing the block; 
    - the "resource" is a list of items that can be scavenged
      around in the block;
    - the "hostile" is a list of monsters that could attack
      on the block;
    - the "amenity". 
   except for the "look", each other field can be empty; symbolized
   by a "None".
   '''
   def __init__(self, look: list, res = None, hostile = None,
      amenity = None):
      super().__init__({
         "look": look,
         "resource": res,
         "hostile": hostile,
         "amenity": amenity
      })
   
   # getters
   def getLook(self) -> list:
      return self.get("look")
   def getResource(self) -> list:
      return self.get("resource")
   def getHostile(self) -> list:
      return self.get("hostile")
   def getAmenity(self) -> int:
      return self.get("amenity")
   
   # toString
   def __str__(self) -> str:
      string = ""
      # look
      for descr in self.get("look"):
         string += descr + '\n'
      # resource
      string += "resource: "
      if self.get("resource") == None:
         string += "None\n"
      else:
         for i, item in enumerate(self.get("resource")):
            string += item.getName()
            if i != len(self.get("resource")) - 1:
               string += ', '
         string += '\n'
      # hostile
      string += "hostile: "
      if self.get("hostile") == None:
         string += "None\n"
      else:
         for i, monsterGen in enumerate(self.get("hostile")):
            string += monsterGen(1).getName()
            if i != len(self.get("hostile")) - 1:
               string += ', '
         string += '\n'
      # add amenity later
      return string

# Block base object
class Block:
   '''a unit spatial content of a dungeon floor. provides a
   name and an explore method to be overriden by sub classes.
   '''
   def __init__(self, name: str, env: Environment):
      self.name = name
      self.env = env
   
   # other
   def printLook(self):
      for l in self.env.getLook():
         print(l);
   
   # exploration
   def explore(self, explorers: Party, haz: int):
      '''sub classes must override this.'''
      print("exploring {}".format(self))
   
   # toString
   def __str__(self) -> str:
      return "{} Block.\n{}".format(self.name, 
         self.env.__str__())

# EmptyBlock object
class EmptyBlock(Block):
   '''a block in which there is no predefined events.'''
   def __init__(self, env: Environment):
      super().__init__("Empty", env)
   
   # exploration
   def explore(self, explorers: Party, haz: int):
      '''just describes the block's environment.'''
      #self.printLook()
      return None # info = None

# ScavengingBlock object      
class ScavengingBlock(Block):
   '''in a scavenging block, you can gather items during
   the exploration of the block.
   '''
   def __init__(self, env: Environment):
      super().__init__("Scavenging", env)
   
   # exploration
   def explore(self, explorers: Party, haz: int):
      '''scavenging has two possible outcomes. as explorers
      try to gather the resource, they might get lucky and
      find something good. else depending on how dangerous
      the block is, they could encounter hostile mobs instead.
      if they manage to survive the fight, they will still
      gather before they leave.
      '''
      #self.printLook()
      info = (list(), None)
      if (rndGen(100) < rndGen(100)): # battle branch
         # DEBUG
         #print("\nyou were looking for goods but found monsters...")
         # scavenging monsters are just a group of a same
         # monster based on the hazard level
         hostile = self.env.get("hostile")
         monsters = list()
         size = rndGen(min(5, rndGen(haz)))
         for i in range(size):
            m = hostile[0](rndGen(haz))
            monsters.append(m)
         battle = BattleState(explorers, Party(monsters))
         info = battle.run()
      # now that's out of the way, scavenge
      if explorers.stillStands(): # scavenging branch
         (qty, item) = (rndGen(5), rnd.choice(self.env.get("resource")))
         print("before:\n", info)
         info = (info[0] + [('i', item.getName()),], info[1])
         print("after:\n", info)
         # DEBUG
         #print("\nyou stumble upon some {}!".format(item.getName()))
         for unit in explorers:
            if not unit.getBag().addMulti(item, qty):
               info = (info[0].append(('p', 
                  "{}'s bag is full!!!".format(unit.getName())), 
                  info[1]))
            # DEBUG
            #print("{} obtained {} x {}.".format(unit.getName(), qty,
               #item.getName()))
      return info

# WoodcuttingBlock object
class WoodcuttingBlock(ScavengingBlock):
   '''in a woodcutting block, you can use an axe if you have one
   to chop down trees and obtain their wood.
   '''
   def __init__(self, env: Environment):
      super().__init__(env)
      self.name = "Woodcutting"
      
   # exploration override
   def explore(self, explorers: Party, haz: int):
      '''test for presence of an axe in the explorers bags.
      if none can be located, rebuke the party. else, run a
      regular scavenging block exploration.
      '''
      found = None
      i = 0
      info = (list(), None)
      while i < len(explorers) and not found:
         found = explorers.getMember(i).getBag().contains("Axe")
         if not found:
            i += 1
      if found:
         info = super().explore(explorers, haz)
      else:
         info = ([('p', "you need an axe to chop trees!"),], None)
      return info
     
# MiningBlock object     
class MiningBlock(ScavengingBlock):
   '''in a mining block, you can use a pickaxe if you have one
   to break rocks and mine for ores or gems.
   '''
   def __init__(self, env: Environment):
      super().__init__(env)
      self.name = "Mining"
      
   # exploration override
   def explore(self, explorers: Party, haz: int):
      '''test for presence of a pickaxe in the explorers bags.
      if none can be located, rebuke the party. else, run a
      regular scavenging block exploration.
      '''
      found = None
      i = 0
      info = (list(), None)
      while i < len(explorers) and not found:
         found = explorers.getMember(i).getBag().contains("Pickaxe")
         if not found:
            i += 1
      if found:
         info = super().explore(explorers, haz)
      else:
         info = ([('p', "you need a pickaxe to mine for ores!!!"),],
            None)
         #print("\nyou need a pickaxe to mine for ores.") # DEBUG
      return info
   
# BattleBlock
class BattleBlock(Block):
   '''the dungeon is full of hostile mobs that will try
   to defeat the party. when this Block is encoutered,
   the explorers will have to fight their way through
   it.'''
   def __init__(self, env: Environment):
      super().__init__("Battle", env)
   
   # exploration
   def explore(self, explorers: Party, haz: int):
      hostile = self.env.get("hostile")
      maxLvl = rndGen(haz)
      # at most 5 monsters. danger level can raise chances of more
      size = rndGen(3)
      for i in range(2):
         if size < 5:
            if rnd.choice(range(100)) < haz * 10: 
               size += 1
      levels = rnd.choices([x + 1 for x in range(maxLvl)], k = size)
      monsters = rnd.choices(hostile, k = size)
      monsters = [monsters[i](levels[i]) for i in range(len(monsters))]
      battle = BattleState(explorers, Party(monsters))
      #self.printLook() # DEBUG
      info = battle.run()
      return info
   
# StairsBlock
class StairsBlock(EmptyBlock):
   '''this is the block that allows you to move to the next level
   of the dungeon. it is also the block that allows you to return
   to the city. its litterally an empty block and has no special
   effect.'''
   def __init__(self):
      super().__init__(
         Environment( 
            ["the stairs to go to the next floor appear before you.",
            "you have completed the exploration of this floor."],
            res = None, hostile = None, amenity = None
         )
      )
      self.name = "Stairs"

# BossBlock
class BossBlock(StairsBlock):
   '''this is a guarded stairs block. it requires the party of
   explorers to defeat a particularly strong monster before they
   can use the stairs.'''
   
   def __init__(self, env: Environment):
      super().__init__() # stairs built
      self.name = "Boss Stairs"
      self.bossRoom = env
      
   # exploration
   def explore(self, explorers: Party, haz: int):
      hostile = self.bossRoom.get("hostile")      
      boss = hostile[0](haz)
      form = 0
      info = (list(), None)
      while explorers.stillStands() and form < boss.getForms():
         print(self.bossRoom.get("look")[form]) # DEBUG
         battle = BattleState(explorers, Party(boss.getNextForm()))
         roundInfo = battle.run()
         # only keep last battle report file
         info = (info[0] + roundInfo[0], roundInfo[1])
         if explorers.stillStands():
            form += 1
      # end of boss battle
      if explorers.stillStands: # defeated the boss
         super().explore()
      # the else will be managed by the exploration code
      return info

# test platform
if __name__ == "__main__":
   pass