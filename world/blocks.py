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
from confrontation import Party
import random as rnd

# Environment object
class Environment(dict):
   '''contains information about what the the inside of a
   block looks like as well as all the resources available
   in it. this information is stored as a dict with multiple
   fields:
    - the "hazard" is a number that describe how dangerous
      the block overall is;
    - the "look" is a list of sentences describing the block; 
    - the "resource" is a list of items that can be scavenged
      around in the block;
    - the "hostile" is a list of monsters that could attack
      on the block;
    - the "amenity". 
   except for the "hazard" and the "look", each other field
   can be empty; symbolized by a "None".
   '''
   def __init__(self, haz: int, look: list, res = None,
      hostile = None, amenity = None):
      super().__init__({
         "hazard": haz,
         "look": look,
         "resource": res,
         "hostile": hostile,
         "amenity": amenity
      })
   
   # getters
   def getHazard(self) -> int:
      return self.get("hazard")
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
      string = "hazard: {:3d}\n".format(self.get("hazard"))
      for descr in self.get("look"):
         string += descr + '\n'
      string += self.get("resource").__str__()
      string += self.get("hostile").__str__()
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
   
   # exploration
   def explore(self, explorers: Party):
      print("exploring {}".format(self))
   
   # toString
   def __str__(self) -> str:
      return "{:8s} Block\n{}".format(self.name, 
         self.env.__str__())

# EmptyBlock object
class EmptyBlock(Block):
   '''a block in which there is no predefined events.'''
   def __init__(self, env: Environment):
      super.__init__("Empty", env)
   
   # exploration
   def explore(self, explorers: Party):
      '''just describes the block's environment.'''
      looks = str()
      for l in self.env.getLook():
         looks += l
         looks += '\n;'
      return looks

# ScavengingBlock object      
class ScavengingBlock(Block):
   '''in a scavenging block, you can gather items during
   the exploration of the block. there are 3 subclasses
   of scavenging blocks which all derive from this one.
   '''
   def __init__(self, name: str, env: Environment):
      super().__init__(name, env)
   
   # exploration
   def explore(self, explorers: Party):
      '''scavenging has two possible outcomes. as explorers
      try to gather the resource, they might get lucky and
      find something good. else depending on how dangerous
      the block is, they could encounter hostile mobs instead.
      '''
      