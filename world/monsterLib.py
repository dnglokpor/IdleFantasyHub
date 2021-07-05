'''
# monsterLib.py
# this module contains methods to that spawn (return new
# instances) of monsters.
# date: 7/5/21
# author: dnglokpor
'''

# imports
import skillLib as skl
import itemLib as itml
from classes import Monster
from elements import NOELM, AEOLA, GAIA, AQUA, VULCAN
from random import choice

# default spawner
def spawn(self, name: str, level: int, bStats: list,
   bSkill: Skill, lore: str, elt = NOELM) -> Monster:
   '''spawn any monster provided with the right info.'''
   return monster = Monster(name, level, bStats, bSkill,
      lore, elt)
   
# spawners
def s_Raccoundrel(level = 1):
   '''return a level "level" Raccoundrel (Monster).'''
   raccoundrel = spawn(
      "Raccoundrel",
      level, 
      [
         12 + choice(5), # hp 12-16
         20 + choice(2), 10 + choice(2), # atk 20-21|def 10-11
         5 + choice(2), 7 + choice(3), # spe 5-6|res 7-9
         6 + choice(2), # dext 6-7
         choice(5) # luc 0-4
      ],
      skl.bite,
      "small raccoun like mob of early dungeon floors with\
 an aggressive behaviour and a vicious bite.",
      NOELM
   )
   # ability/critical skills
   
   # drops
   # a single pelt
   raccoundrel.getBag().add(itml.pelt.copy())
   
   # done so return
   return raccoundrel
)
def s_Sparowl(level = 1):
   '''return a level "level" Sparowl (Monster).'''
   sparowl = spawn(
      "Sparowl",
      level,
      [
         10 + choice(5), # hp 10-14
         20 + choice(2), 8 + choice(2), # atk 20-21|def 8-10
         15 + choice(3), 9 + choice(3), # spe 15-17|res 9-11
         10 + choice(2), # dext 10-11
         choice(5) # luc 0-4
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
   for time in range(5)
      sparowl.getBag().add(itml.smallFeathers)
   
   # return 
)