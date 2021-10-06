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

# res folder
ITEMS = "world/resource/items/"
GEAR = "world/resource/gear/"
if __name__ == "__main__":
   ITEMS = "resource/items/"
   GEAR = "resource/gear/"
# gear are by category so I can reuse the same ico with
# diverse background to say quality:
# grey -> green -> blue -> purple -> red

# items
# # Pelt
pelt = Item(
   "Pelt",
   "freshly skinned pelt of a small dungeon denizen.",
   10
)
# # small feathers
smallFeathers = Item(
   "Small Feathers",
   "a few small but sturdy feathers that float in the wind.",
   5
)
smallFeathers.setIco(ITEMS + "glitch-icon-24.png")
# # Honee
honee = Item(
   "Honee",
   "Honeybeat species honey. it is a lot darker than regular honey "
   "because of its high caramelized fructose contents. makes "
   "great taffy.",
   15
)
honee.setIco(ITEMS + "glitch-icon-54.png")
# # Stinger
stinger = Item(
   "Stinger",
   "freshly harvested Honeybeat species stinger. apothecaries "
   "extract toxins from it to make a variety of potions.",
   8
)
# # Silk
silk = Item(
   "Silk",
   "a ball of bug silk recovered from a bug-like monster. it is "
   "highly durable and enter the fabrication of textiles.",
   15
)
# # Monster Egg
monsterEgg = Item(
   "Monster Egg",
   "the egg of a creature from the dungeon. What would hatch from "
   "this? usually people prefer not to find out.",
   20
)
monsterEgg.setIco(ITEMS + "glitch-icon-71.png")
# # Compound Eye
compoundEye = Item(
   "Compound Eye",
   "the compound eyes of a bug-like monster. alchemists use them "
   "to manufacture powerful potions that help with sight.",
   30
)
# # Bug Wing
bugWing = Item(
   "Bug Wing",
   "a giant silver coloured butterfly wing. it is pretty lightweight "
   "and durable. they are hard to come around so merchants pay a "
   "a good price for them.",
   50
)

# herbs
# # Chemomille
chemomille = Item(
   "Chemomille",
   "a yellowish small flower that smells like apples. "
   "its rich constitution makes it prime remedy ingredient.",
   10
)
chemomille.setIco(ITEMS + "glitch-icon-97.png")
# # Wild Corn
wildCorn = Item(
   "Wild Corn",
   "just like normal corn but found in the grass lands of the "
   "dungeon. They are magically delicious.",
   5
)
wildCorn.setIco(ITEMS + "glitch-icon-51.png")
# # Violette
violette = Item(
   "Violette",
   "this purple flower buds on the early floors of the dungeon. "
   "it has no specific use but sure is pretty to look at.",
   5
)
violette.setIco(ITEMS + "glitch-icon-96.png")
# # Orangerry
orangerry = Item(
   "Orangerry",
   "this berry grows in damp soiled clearings of forests. "
   "its fragrant flowers attract varieties of monsters.",
   10
)
orangerry.setIco(ITEMS + "44.png")

# wood
# # Hauk Wood
haukWood = Item(
   "Hauk Wood",
   "small logs from a felled Hauk tree. the dark bark conceals"
   " lightly colored durable wood underneath it.",
   15
)
haukWood.setIco(ITEMS + "glitch-icon-41.png")
# Yellow Foot
yellowFoot = Item(
   "Yellow Foot",
   "this small mushroom loves to grow at the base of trees, preferably "
   "where the sun doesn't shine.",
   5
)
yellowFoot.setIco(ITEMS + "glitch-icon-61.png")

# ores
# # Iron Ore
ironOre = Item(
   "Iron Ore",
   "small rock shards containing significant traces of iron.",
   10
)
ironOre.setIco(ITEMS + "glitch-icon-23.png")
# # Palemethyst Shard
palemethystShard = Item(
   "Palemethyst Shard",
   "a shard of a variety of quartz with a really pale purple hue. "
   "they're often used in the confection of cheap house furniture.",
   10
)
palemethystShard.setIco(ITEMS + "7.png")

# merchandise
# # Arrow
arrow = Item(
   "Arrow",
   "40cm of wood crowned by a sharpened steel head and\
 feathers in the back. rangers' favorite.", 
   1
)
arrow.setIco(GEAR + "Grey/Arrows/ScoutArrow.png")
# # Axe
axe = Item(
   "Axe",
   "a small woodcutter axe made of steel. handy when you seek "
   "good lumber.",
   250
)
axe.setIco(GEAR + "Grey/MeleeWeapon1H/WoodcutterAxe.png")
# # Pickaxe
pickaxe = Item(
   "Pickaxe",
   "rocks tremble in fear when they see you wield this robust "
   "miner pickaxe. use without moderation.",
   250
)
pickaxe.setIco(ITEMS + "glitch-icon-60.png")

# weapons
# # Short Sword
shortSword = Sword(
   "Short Sword",
   "this sword is about a elbow to fingertips long. "
   "it's just as deadly as any other sword thought.",
   60,
   [("attack", 6),]
)
shortSword.setIco(GEAR + 
   "Grey/MeleeWeapon1H/ShortSword_[Paint].png")
# # longbow
longbow = Bow(
   "Longbow",
   "a meter-long twig arched into a bow shape by a piece of "
   "fine hemp rope.",
   60,
   [("attack", 4), ("dexterity", 1)]
)
longbow.setIco(GEAR + "Grey/Bows/ScoutBow.png")
# # Walking Stick
walkingStick = Staff(
   "Walking Stick",
   "a fine piece of wood as useful as a support cane as it "
   " is a magic catalyst.",
   60,
   [("special", 8),]
)
walkingStick.setIco(GEAR + "Grey/MeleeWeapon1H/HardwoodWand.png")

# armors
# # Go Getup
goGetup = Armor(
   "Go Getup",
   "jacket wore on plain clothes and sturdy canvas pants\
 for one going on an adventure.", 
   60, 
   [("defense", 5),]
)
goGetup.setIco(GEAR + "Grey/Armor/Scout_[Paint].png")

# accessories
# # Leather Boots
leatherBoots = Accessory(
   "Leather Boots",
   "worn out leather shoes of acceptable quality. no nail nor "
   "thorn will make it to your foot in these.",
   60,
   [("defense", 1),]
)
leatherBoots.setIco(GEAR + "Grey/Boots/LeatherJacket.png")
# # Gloves
gloves = Accessory(
   "Gloves",
   "a simple pair of worn out cotton gloves. help with grip and "
   "handling.",
   60,
   [("attack", 1),]
)
gloves.setIco(GEAR + "Grey/Gloves/Hunter.png")