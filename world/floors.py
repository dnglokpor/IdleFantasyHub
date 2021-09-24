'''
# floors.py
# a floor is a randomly constructed collection of blocks.
# exploring a floor means clearing every block in it and r
# eaching the stairs without dying.
# date: 9/22/21
# author: dnglokpor
'''

# imports
from blocks import Block, StairsBlock
import random as rnd

# Floor object
class Floor:
   '''a dungeon floor is a collection of blocks. it has a size that
   is the number of blocks it is made of; including the stairs block
   that is the end of the floor. the arrangement of the blocks thought
   is random but based on how many of each blocks there is.
   '''
   def __init__(self, size: int):
      '''only the size of it is needed for the initial build.'''
      self.size = size
      
   # getters
   def getSize(self) -> int:
      return self.size
   
   # randomly generate floor
   def build(self, pop: list, probs: list, stairs: Block, 
      debug = False) -> list:
      '''this uses the two lists to fill up the floor with
      blocks randomly choosen meaning "probs" contains how
      many of each block is needed to fill "size -1" slots 
      of this floor. this requires that 
      "len(pop) == len(probs)". if the debug argument is set to
      "True", the floor composition will be console printed.
      the created list is returned.
      '''
      if pop == None or probs == None:
         raise Exception("blocks passed are not valid!")
      elif len(pop) != len(probs):
         raise Exception("argument lists of different sizes!")
      elif sum(probs) != self.size - 1:
         raise Exception("unsufficient probs!")
      else:
         # build list
         build = rnd.choices(pop, probs, k = self.size - 1)
         # deterministic alternative
         '''
         for bType in range(len(pop)):
            for no in range(probs[bType]):
               build.append(pop[bType])
         rnd.shuffle(build) # shuffle the order
         '''
         build.append(stairs)
         if debug:
            for no, b in enumerate(build):
               print("{}f: {}".format(no + 1, b))
               print('\n')
         return build
         
# Stratum