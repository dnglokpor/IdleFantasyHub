'''
# monsterLib.py
# this module contains methods to that spawn (return new
# instances) of monsters.
# date: 7/5/21
# author: dnglokpor
'''

# imports
from elements import NOELM, AEOLA, GAIA, AQUA, VULCAN
from skills import Skill
from units import Monster
import itemLib as il
import skillLib as skl
from random import seed, choice

# helper 
def choose(maxVal) -> int:
   '''return a random value from 0 to "maxVal - 1".'''
   seed() # seed rnd gen
   return choice(range(maxVal))

# default spawner
def spawn(name: str, level: int, bStats: list,
   bSkill: Skill, lore: str, elt = NOELM) -> Monster:
   '''spawn any monster provided with the right info.'''
   return Monster(name, level, bStats, bSkill, lore, elt)
   
# monster spawners
# Raccoundrel
def s_Raccoundrel(level = 1):
   '''return a level "level" Raccoundrel (Monster).'''
   raccoundrel = spawn(
      "Raccoundrel",
      level, 
      [
         15 + choose(3), # hp 15-17
         20 + choose(2), 10 + choose(2), # atk 20-21|def 10-11
         5 + choose(2), 7 + choose(3), # spe 5-6|res 7-9
         6 + choose(2), # dext 6-7
         choose(5) # luc 0-4
      ],
      skl.bite,
      "small raccoun like mob of early dungeon floors with\
 an aggressive behaviour and a vicious bite.",
      NOELM
   )
   # ability/critical skills
   
   # drops
   # pelt x 1
   raccoundrel.getBag().add(il.s_Pelt())
   
   # done so return
   return raccoundrel

# Sparowl
def s_Sparowl(level = 1):
   '''return a level "level" Sparowl (Monster).'''
   sparowl = spawn(
      "Sparowl",
      level,
      [
         12 + choose(5), # hp 10-14
         20 + choose(2), 8 + choose(2), # atk 20-21|def 8-10
         15 + choose(3), 9 + choose(3), # spe 15-17|res 9-11
         10 + choose(2), # dext 10-11
         choose(5) # luc 0-4
      ],
      skl.peck,
      "this giant dungeon owl is incredibly agile so watch\
 out for its sharp beak and powerful wind bursts.",
      AEOLA
   )
   # ability/critical skills
   if level >= 3:
      sparowl.getSkillSet().assign("ability", skl.whoosh)
   
   # drops
   # feathers x 5
   sparowl.getBag().addMulti(il.s_SmallFeathers(), 5)
   
   # return
   return sparowl

# Honeybeat
def s_Honeybeat(level = 1):
   '''return a level "level" Honeybeat (Monster).'''
   honeybeat = spawn(
      "Honeybeat",
      level,
      [
         12 + choose(5), # hp 10-14
         18 + choose(5), 6 + choose(3), # atk 18-22|def 6-8
         8 + choose(3), 15 + choose(3), # spe 8-10|res 15-17
         15 + choose(4), # dext 15-18
         choose(5) # luc 0-4
      ],
      skl.sting,
      "everyone likes honey but if you come accros a Honeybeat "
      "hive, you should run away unless being lethally stung "
      "is the last thing on your bucket list.",
      AEOLA
   )
   # ability/critical skills
   if level >= 1:
      honeybeat.getSkillSet().assign("ability", skl.buzz)
   
   # drops
   # stinger x 1, honee x 1
   honeybeat.getBag().add(il.s_Stinger())
   honeybeat.getBag().add(il.s_Honee())
   
   # return
   return honeybeat

# Caterkiller
def s_Caterkiller(level = 1):
   '''return a level "level" Caterkiller (Monster).'''
   caterkiller = spawn(
      "Caterkiller",
      level, 
      [
         10 + choose(3), # hp 10-12
         15 + choose(5), 13 + choose(2), # atk 15-19|def 13-14
         10 + choose(2), 12 + choose(3), # spe 10-11|res 12-12
         4 + choose(2), # dext 4-5
         choose(5) # luc 0-4
      ],
      skl.bite,
      "don't let this giant caterpillar fool you. thanks to their "
      "speed debuffs and their persistence, they have claimed many ",
      "adventurers lives.",
      AEOLA
   )
   # ability/critical skills
   if level >= 1:
      caterkiller.getSkillSet().assign("ability", skl.silkKnit)
   
   # drops
   # silk x 2
   caterkiller.getBag().addMulti(il.s_Silk(), 2)
   
   # done so return
   return caterkiller