'''
# dungeon.py
# the dungeon is a mystical labyrinth that the adventurers of 
# IdleFantasyHub must explore. it contains multiple floors
# broken into stratums. each stratum contains 5 floors and
# showcase a unique environment and ecology. a floor is a
# randomly constructed collection of blocks. exploring a floor
# means clearing every block in it and reaching the stairs 
# without dying.
# this module is a library where the all levels are defined.
# the dungeon itself will be a dict with the floor number 
# as key and value being the actual levels.
# date: 9/23/21
# author: dnglokpor
'''

# imports
import itemLib as il
import monsterLib as ml
import bossLib as bl
from blocks import Environment, EmptyBlock, ScavengingBlock,\
   WoodcuttingBlock, MiningBlock, BattleBlock, StairsBlock,\
   BossBlock
from floors import Floor

# first stratum: Viridian Greens
# 1f - 2f: prairie, 3f - 5f: forest
# blocks list
prairieEB = EmptyBlock(
   Environment(
      ["There is lush green tall grass all around the place. "
       "The wind blows slowly among the small bushes. "
       "Bugs can be heard chirping gladly in the sunlight.",
      ],
      res = None,
      hostile = None, 
      amenity = None
   )
)
prairieSB = ScavengingBlock(
   Environment(
      ["the prairie seems ripe with fragrant plants and flowers. "
      "herb picking would definitely yield results.",
      ],
      res = [il.s_Chemomille, il.s_WildCorn, il.s_Violette],
      hostile = [ml.s_Sparowl],
      amenity = None
   )
)
prairieBB = BattleBlock(
   Environment(
      look = 
      ["a sudden air of danger float around the prairie. "
       "something moves in the grass in front of the party. "
       "weapons in hand the party welcome the monsters...",
      ],
      res = None,
      hostile = [ml.s_Raccoundrel, ml.s_Sparowl],
      amenity = None
   )
)
forestEB = EmptyBlock(
   Environment(
      ["huge trees all around you have cut off the sunlight. "
      "wings beating and bug buzzes can be heard coming from "
      "here and there. a damp and moist fragrance hits your "
      "nostrils.",
      ],
      res = None,
      hostile = None, 
      amenity = None
   )
)
forestSB = ScavengingBlock(
   Environment(
      ["small fragrants plants seem to grow all around this clearing. "
      "herb picking would definitely yield results.",
      ],
      res = [il.s_Chemomille, il.s_Orangerry],
      hostile = [ml.s_Sparowl],
      amenity = None
   )
)
forestWB = WoodcuttingBlock(
   Environment(
      ["the trees that grow around here seem to be of good quality. "
       "logging here could turn out profitable.",
      ],
      res = [il.s_HaukWood, il.s_YellowFoot],
      hostile = [ml.s_Honeybeat],
      amenity = None
   )
)
forestBB = BattleBlock(
   Environment(
      look = 
      ["the trees around you suddenly feel quite threatening. "
      "something is observing you; and its not welcoming. "
      "you barely get to your weapons that it is upon you.",
      ],
      res = None,
      hostile = [ml.s_Raccoundrel, ml.s_Sparowl, ml.s_Caterkiller],
      amenity = None
   )
)
forestBoB = BossBlock(
   Environment(
      look = [
      "you arrive to the stairs that lead to the next floor. but "
      "you can't take them because something is nesting on it. "
      "in the middle of the web barring your path, you see a pupa."
      "not so happy to be troubled, it attacks you...",
      "the pupa breaks but you can't rejoice because something fell "
      "from it. you watch as it stretches its wings and screams at "
      "you. the butterfly hatched sooner than expected and its not "
      "too content of that..."
      ],
      res = None,
      hostile = [bl.s_Butterfreak],
      amenity = None
   )
)

# floors list
floor1 = Floor(
   size = 6,
   hazard = 1,
   pop = [prairieEB, prairieBB, prairieSB], 
   probs = [2, 2, 1],
   stairs = StairsBlock()
)
floor2 = Floor(
   size = 7,
   hazard = 1,
   pop = [prairieEB, prairieBB, prairieSB], 
   probs = [2, 3, 1],
   stairs = StairsBlock()
)
floor3 = Floor(
   size = 8,
   hazard = 2,
   pop = [forestEB, forestBB, forestWB], 
   probs = [3, 3, 1],
   stairs = StairsBlock()
)
floor4 = Floor(
   size = 9,
   hazard = 2,
   pop = [forestEB, forestBB, forestSB], 
   probs = [3, 4, 1],
   stairs = StairsBlock()
)
floor5 = Floor(
   size = 10,
   hazard = 3,
   pop = [forestEB, forestBB, forestSB, forestWB], 
   probs = [3, 4, 1, 1],
   stairs = forestBoB
)

# dungeon
DUNGEON = {
   1: floor1, 2: floor2, 3: floor3, 4: floor4, 5: floor5
}