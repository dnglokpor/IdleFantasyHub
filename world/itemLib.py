'''
# itemLib.py
# this module contains predefined items that can be collected
# by units (in their bags).
# date: 7/4/21
# author: dnglokpor
'''

# imports
from collectibles import Item, Sword, Spear, Bow, Artillery,\
 Staff, Tome, Armor, Accessory

# items
arrow = Item(
   "Arrow",
   "40cm of wood crowned by a sharpened steel head and\
 feathers in the back. rangers' favorite.", 
   1
)
pelt = Item(
   "Pelt",
   "freshly skinned pelt of a small dungeon denizen.",
   10
)
smallFeathers = Item(
   "Small Feathers",
   "a few small but sturdy feathers that float in the wind.",
   5
)

# weapons
longsword = Sword(
   "Longsword",
   "an arm-long sword made of greyish steel. watch\
 out for cuts.",
   60,
   [("attack", 6),]
)
longbow = Bow("Longbow",
   "a meter-long twig arched into a bow shape by a piece\
 of fine hemp rope.",
   60,
   [("attack", 4), ("dexterity", 1)]
)
walkingStick = Staff("Walking Stick",
   "a fine piece of wood as useful as support cane as it\
 a magic catalyst.",
   60,
   [("special", 8),]
)

# armors
goGetup = Armor("Go Getup",
   "jacket wore on plain clothes and sturdy canvas pants\
 for one going on an adventure.", 
   60, 
   [("defense", 5),]
)

# accessories

if __name__ == "__main__":
   dup = pelt.copy()
   print(pelt, dup)
   print("same item? ", longbow == dup)
