'''
# bossLib.py
# similar to monsterLib.py, this module contains prebuilt BossMonsters
# and ways to easily spawn them.
# date: 9/25/21
# author: dnglokpor
'''

# imports
from elements import NOELM, AEOLA, GAIA, AQUA, VULCAN
from skills import Skill
from units import Monster, BossMonster
import itemLib as il
import skillLib as skl
from monsterLib import choose, spawn

# boss spawners
# Butterfreak
def s_Butterfreak(level = 1):
   '''return a level "level" Butterfreak.'''
   butterfreak = BossMonster()
   # cocoon form
   pupa = spawn(
      "Butterfreak (pupa)",
      level,
      [
         30 + choose(6), # hp 30-35
         5 + choose(3), 15 + choose(2), # atk 5-7|def 15-16
         5 + choose(3), 15 + choose(2), # spe 5-7|res 15-16
         10 + choose(3), # dext 10-12
         choose(7) # luc 0-6
      ],
      skl.cocoon,
      "when a Caterkiller has gathered nutrients for a year, "
      "it wraps itself into its silk, making this pupa. the cocoon "
      "protect it while it reorganizes its organs into its adult "
      "form.",
      AEOLA
   )
   # ability/critical
   pupa.getSkillSet().assign("ability", skl.whine)
   # drops
   # nothing
   
   # butterfly form
   butterfly = spawn(
      "Butterfreak (butterfly)",
      level,
      [
         50 + choose(6), # hp 30-35
         20 + choose(3), 12 + choose(4), # atk 20-22|def 12-15
         18 + choose(3), 12 + choose(4), # spe 18-20|res 15-15
         15 + choose(2), # dext 15-16
         choose(7) # luc 0-6
      ],
      skl.sting,
      "a fully mature caterkiller. although quite short lived, this "
      "giant butterfly monster's presence wreaks havoc in the "
      "dungeon ecosystem. they feed on all they can find to fuel "
      "their egg-laying. this includes unlucky adventurers as well.",
      AEOLA
   )
   # ability/critical
   butterfly.getSkillSet().assign("ability", skl.tornado)
   # drops
   # monster egg x 5 ,compound eye x 2, bug wing x 2
   butterfly.getBag().addMulti(il.s_MonsterEgg(), 5)
   butterfly.getBag().addMulti(il.s_CompoundEye(), 2)
   butterfly.getBag().addMulti(il.s_BugWing(), 2)
   
   # add forms to boss
   print("pupa stats:\n", pupa.getStats())
   print("butterfly stats:\n", butterfly.getStats())
   butterfreak.addForm(pupa)
   butterfreak.addForm(butterfly)
   
   return butterfreak
