'''
# bestiary.py
# this module contains the Bestiary object which is really just a
# a dictionary that maps the names of monsters in lowercase to their
# their spawners so that monster can be spawned and information
# about it can be drawned.
# date: 10/06/21
# author: dnglokpor
'''

# imports
import monsterLib as ml
import bossLib as bl

# bestiary
BESTIARY = {
   # # mobs
   "raccoundrel": (1, ml.s_Raccoundrel),
   "sparowl": (2, ml.s_Sparowl),
   "honeybeat": (3, ml.s_Honeybeat),
   "caterkiller": (4, ml.s_Caterkiller),
   # # bosses
   "butterfreak": (5, bl.s_Butterfreak)
}