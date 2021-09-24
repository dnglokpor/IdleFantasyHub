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
honee = Item(
   "Honee",
   "Honeybeat species honey. it is a lot darker than regular honey "
   "because of its high caramelized fructose contents. makes "
   "great taffy.",
   15
)
stinger = Item(
   "Stinger",
   "freshly harvested Honeybeat species stinger. apothecaries "
   "extract toxins from it to make a variety of potions.",
   8
)

# herbs
chemomille = Item(
   "Chemomille",
   "a yellowish small flower that smells like apples. "
   "its rich constitution makes it prime remedy ingredient.",
   10
)
dandetigreSeeds = Item(
   "Dandetigre Seeds",
   "these seeds are known for being carried long distance by"
   " winds. the prairie is not complete without them.",
   2
)
theestleNeedles = Item(
   "Theestle Needles",
   "the needles of this small plant are a lot harder than "
   "wood should be. artisans use them as nail replacement.",
   5
)

# wood
haukWood = Item(
   "Hauk Wood",
   "small logs from a felled Hauk tree. the dark bark conceals"
   " lightly colored durable wood underneath it.",
   15
)
hardcorn = Item(
   "Hardcorn",
   "nuts commonly found while felling Hauk trees. they're so hard "
   "literally nothing eats them. prized crafting ingredient.",
   5
)

# ores
ironOre = Item(
   "Iron Ore",
   "small rock shards containing significant traces of iron.",
   10
)
palemethyst = Item(
   "Palemethyst",
   "a variety of quartz with a really pale purple hue. they're "
   "often used in the confection of cheap house furniture.",
   10
)

# tools
axe = Item(
   "Axe",
   "a small woodcutter axe made of steel. handy when you seek "
   "good lumber.",
   250
)
pickaxe = Item(
   "Pickaxe",
   "rocks tremble in fear when they see you wield this robust "
   "miner pickaxe. use with moderation",
   250
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
   pass 