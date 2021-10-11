'''
# itemLib.py
# this module contains predefined items that can be collected
# by units (in their bags).
# date: 7/4/21
# author: dnglokpor
# update 10/6/21: replaced autobuilt Item objects by spawners
# instead allowing for only on demand construction.
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
def s_Pelt():
   '''return a Pelt Item.'''
   pelt = Item(
      "Pelt",
      "freshly skinned pelt of a small dungeon denizen.",
      10
   )
   return pelt
# # small feathers
def s_SmallFeathers():
   '''return a small feathers Item.'''
   smallFeathers = Item(
      "Small Feathers",
      "a few small but sturdy feathers that float in the wind.",
      5
   )
   smallFeathers.setIco(ITEMS + "glitch-icon-24.png")
   return smallFeathers
# # Honee
def s_Honee():
   '''return a Honee Item.'''
   honee = Item(
      "Honee",
      "Honeybeat species honey. it is a lot darker than regular honey "
      "because of its high caramelized fructose contents. makes "
      "great taffy.",
      15
   )
   honee.setIco(ITEMS + "glitch-icon-54.png")
   return honee
# # Stinger
def s_Stinger():
   '''return a Stinger Item.'''
   stinger = Item(
      "Stinger",
      "freshly harvested Honeybeat species stinger. apothecaries "
      "extract toxins from it to make a variety of potions.",
      8
   )
   return stinger
# # Silk
def s_Silk():
   '''return a Silk Item.'''
   silk = Item(
      "Silk",
      "a thread of bug silk recovered from a bug-like monster. it is "
      "highly durable and enter the fabrication of textiles.",
      15
   )
   silk.setIco(ITEMS + "glitch-icon-59.png")
   return silk
# # Monster Egg
def s_MonsterEgg():
   '''return a Monster Egg Item.'''
   monsterEgg = Item(
      "Monster Egg",
      "the egg of a creature from the dungeon. What would hatch from "
      "this? usually people prefer not to find out.",
      20
   )
   monsterEgg.setIco(ITEMS + "glitch-icon-71.png")
   return monsterEgg
# # Compound Eye
def s_CompoundEye():
   '''return a Compound Eye Item.'''
   compoundEye = Item(
      "Compound Eye",
      "the compound eyes of a bug-like monster. alchemists use them "
      "to manufacture powerful potions that help with sight.",
      30
   )
   return compoundEye
# # Bug Wing
def s_BugWing():
   '''return a Bug Wing Item.'''
   bugWing = Item(
      "Bug Wing",
      "a giant silver coloured butterfly wing. it is pretty lightweight "
      "and durable. they are hard to come around so merchants pay a "
      "a good price for them.",
      50
   )
   return bugWing

# herbs
# # Chemomille
def s_Chemomille():
   '''return a Chemomille Item.'''
   chemomille = Item(
      "Chemomille",
      "a yellowish small flower that smells like apples. "
      "its rich constitution makes it prime remedy ingredient.",
      10
   )
   chemomille.setIco(ITEMS + "glitch-icon-97.png")
   return chemomille
# # Wild Corn
def s_WildCorn():
   '''return a Wild Corn Item.'''
   wildCorn = Item(
      "Wild Corn",
      "just like normal corn but found in the grass lands of the "
      "dungeon. They are magically delicious.",
      5
   )
   wildCorn.setIco(ITEMS + "glitch-icon-51.png")
   return wildCorn
# # Violette
def s_Violette():
   '''return a Violette Item.'''
   violette = Item(
      "Violette",
      "this purple flower buds on the early floors of the dungeon. "
      "it has no specific use but sure is pretty to look at.",
      5
   )
   violette.setIco(ITEMS + "glitch-icon-96.png")
   return violette
# # Orangerry
def s_Orangerry():
   '''return a Orangerry Item.'''
   orangerry = Item(
      "Orangerry",
      "this berry grows in damp soiled clearings of forests. "
      "its fragrant flowers attract varieties of monsters.",
      10
   )
   orangerry.setIco(ITEMS + "44.png")
   return orangerry

# wood
# # Hauk Wood
def s_HaukWood():
   '''return a Hauk Wood Item.'''
   haukWood = Item(
      "Hauk Wood",
      "small logs from a felled Hauk tree. the dark bark conceals"
      " lightly colored durable wood underneath it.",
      15
   )
   haukWood.setIco(ITEMS + "glitch-icon-41.png")
   return haukWood
# Yellow Foot
def s_YellowFoot():
   '''return a Yellow Foot Item.'''
   yellowFoot = Item(
      "Yellow Foot",
      "this small mushroom loves to grow at the base of trees, preferably "
      "where the sun doesn't shine.",
      5
   )
   yellowFoot.setIco(ITEMS + "glitch-icon-61.png")
   return yellowFoot

# ores
# # Iron Ore
def s_IronOre():
   '''return a Iron Ore Item.'''
   ironOre = Item(
      "Iron Ore",
      "small rock shards containing significant traces of iron.",
      10
   )
   ironOre.setIco(ITEMS + "glitch-icon-23.png")
   return ironOre
# # Palemethyst Shard
def s_PalemethystShard():
   '''return a Palemethyst Shard Item.'''
   palemethystShard = Item(
      "Palemethyst Shard",
      "a shard of a variety of quartz with a really pale purple hue. "
      "they're often used in the confection of cheap house furniture.",
      10
   )
   palemethystShard.setIco(ITEMS + "7.png")
   return palemethystShard

# merchandise
# # Arrow
def s_Arrow():
   '''return a Arrow Item.'''
   arrow = Item(
      "Arrow",
      "40cm of wood crowned by a sharpened steel head and feathers "
      "in the back. rangers' favorite.", 
      1
   )
   arrow.setIco(GEAR + "Grey/Arrows/ScoutArrow.png")
   return arrow
# # Axe
def s_Axe():
   '''return a Axe Item.'''
   axe = Item(
      "Axe",
      "a small woodcutter axe made of steel. handy when you seek "
      "good lumber.",
      250
   )
   axe.setIco(GEAR + "Grey/MeleeWeapon1H/WoodcutterAxe.png")
   return axe
# # Pickaxe
def s_Pickaxe():
   '''return a Pickaxe Item.'''
   pickaxe = Item(
      "Pickaxe",
      "rocks tremble in fear when they see you wield this robust "
      "miner pickaxe. use without moderation.",
      250
   )
   pickaxe.setIco(ITEMS + "glitch-icon-60.png")
   return pickaxe

# weapons
# # Short Sword
def s_ShortSword():
   '''return a Short Sword weapon.'''
   shortSword = Sword(
      "Short Sword",
      "this sword is about a elbow to fingertips long. "
      "it's just as deadly as any other sword thought.",
      60,
      [("attack", 6),]
   )
   shortSword.setIco(GEAR + "Grey/MeleeWeapon1H/ShortSword_[Paint].png")
   return shortSword
# # longbow
def s_Longbow():
   '''return a Longbow weapon.'''
   longbow = Bow(
      "Longbow",
      "a meter-long twig arched into a bow shape by a piece of "
      "fine hemp rope.",
      60,
      [("attack", 4), ("dexterity", 1)]
   )
   longbow.setIco(GEAR + "Grey/Bows/ScoutBow.png")
   return longbow
# # Walking Stick
def s_WalkingStick():
   '''return a Walking Stick weapon.'''
   walkingStick = Staff(
      "Walking Stick",
      "a fine piece of woodcraft as useful as a support cane as it "
      " is a magic catalyst.",
      60,
      [("special", 8),]
   )
   walkingStick.setIco(GEAR + "Grey/MeleeWeapon1H/HardwoodWand.png")
   return walkingStick

# armors
# # Go Getup
def s_GoGetup():
   '''return a Go Getup Armor.'''
   goGetup = Armor(
      "Go Getup",
      "jacket wore on plain clothes and sturdy canvas pants for "
      "one going on an adventure.", 
      60, 
      [("defense", 5),]
   )
   goGetup.setIco(GEAR + "Grey/Armor/Scout_[Paint].png")
   return goGetup

# accessories
# # Leather Boots
def s_LeatherBoots():
   '''return a Leather Boots Accessory.'''
   leatherBoots = Accessory(
      "Leather Boots",
      "worn out leather shoes of acceptable quality. no nail nor "
      "thorn will make it to your foot in these.",
      60,
      [("defense", 1),]
   )
   leatherBoots.setIco(GEAR + "Grey/Boots/LeatherJacket.png")
   return leatherBoots
# # Gloves
def s_Gloves():
   '''return a Gloves Accessory.'''
   gloves = Accessory(
      "Gloves",
      "a simple pair of worn out cotton gloves. help with grip and "
      "handling.",
      60,
      [("attack", 1),]
   )
   gloves.setIco(GEAR + "Grey/Gloves/Hunter.png")
   return gloves