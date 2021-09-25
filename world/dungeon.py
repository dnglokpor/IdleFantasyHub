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
from blocks import Environment, StairsBlock
from floors import Floor

# first stratum: Viridian Green Plains
# 1f - 2f: prairie, 3f - 5f: forest
# blocks list
prairieEB = EmptyBlock(
   Environment(
      ["There is lush green tall grass all around the place.",
       "The wind blows slowly among the small bushes.",
       "Bugs can be heard chirping gladly in the sunlight."
      ],
      res = None,
      hostile = None, 
      amenity = None
   )
)
prairieSB = ScavengingBlock(
   Environment(
      ["the prairie seems ripe with fragrant plants and flowers.",
      "herb picking would definitely yield results.",
      ],
      res = [il.chemomille, il.dandetigreSeeds, il.theestleNeedles],
      hostile = [ml.s_Sparowl],
      amenity = None
   )
)
prairieBB = BattleBlock(
   Environment(
      look = 
      ["a sudden air of danger float around the prairie.",
       "something moves in the grass in front of the party.",
       "weapons in hand the party welcome the monsters..."
      ],
      res = None,
      hostile = [ml.s_Raccoundrel, ml.s_Sparowl],
      amenity = None
   )
)
forestEB = EmptyBlock(
   Environment(
      ["Huge trees all around you have cut off the sunlight.",
      "wings beating and bug buzzes can be heard coming from "
      "here and there.",
       "A damp and moist fragrance hits your nostrils."
      ],
      res = None,
      hostile = None, 
      amenity = None
   )
)
forestSB = ScavengingBlock(
   Environment(
      ["small fragrants plants seem to grow all around this clearing.",
      "herb picking would definitely yield results.",
      ],
      res = [il.chemomille, il.orangerry],
      hostile = [ml.s_Sparowl],
      amenity = None
   )
)
forestWB = WoodcuttingBlock(
   Environment(
      ["the trees that grow around here seem to be of good quality.",
       "logging here could turn out profitable.",
      ],
      res = [il.haukWood, il.hardcorn],
      hostile = [ml.s_Honeybeat],
      amenity = None
   )
)
forestBB = BattleBlock(
   Environment(
      look = 
      ["the trees around you suddenly feel quite threatening.",
      "something is observing you; and its not welcoming.",
      "you barely get to your weapons that it is upon you."
      ],
      res = None,
      hostile = [ml.s_Raccoundrel, ml.s_Sparowl, ml.s_caterkiller],
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
   stairs = BossBlock()
)

# dungeon
