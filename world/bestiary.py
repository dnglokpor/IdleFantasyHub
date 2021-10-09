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
   "raccoundrel": ml.s_Raccoundrel,
   "sparowl": ml.s_Sparowl,
   "honeybeat": ml.s_Honeybeat,
   "caterkiller": ml.s_Caterkiller,
   # # bosses
   "butterfreak": bl.s_Butterfreak
}