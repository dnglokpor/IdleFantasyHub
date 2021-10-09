'''
# picsGen.py
# this module's goal is to generate edited pictures that represent
# element of the game in a way to make it more visual and more 
# appealing than text (since text in discord is hard to style).
# date: 9/29/21
# author: dnglokpor
'''

# imports
import sys, os
from PIL import Image
from PIL.ImageFont import truetype
from PIL.ImageDraw import Draw
from idleUser import IdleUser

# add game world package to path so that internal imports work
sys.path.insert(0, 
   "D:/myLewysG/Logiciels/Mes Tests/IdleFantasyHub/world")

from world.base import STATS, UnitStats
from world.collectibles import Gear

# constants
PAGES = "world/resource/pages/"
OUTPUT = "records/generated/"
PROFILE = "profile.png"
BAG = "inventory.png"
ITEMS = "world/resource/items/"
DEFAULT = ITEMS + "glitch-icon-87.png"
ITEM = "item.png"

# profile page
def genProfile(user: IdleUser) -> str:
   ''' uses PIL image processing capabilities to add text boxes
   and pictures to a premade image outputting a collage representing
   the profile page of a player.'''
   # set up
   base = Image.open(PAGES + PROFILE) # load original picture
   base = base.copy() # make copy to not lose base
   editor = Draw(base) # make drawing context on base

   # profile picture
   pp = Image.open(user.getPicture())
   pp = pp.resize((181, 175))
   base.paste(pp, (62, 112))
   # name
   nameField = user.getUname()
   if user.hasHero():
      nameField += " [{}]".format(user.getHero().getClassName())
   editor.text(
      (410, 125),
      nameField,
      font = truetype("bahnschrift.ttf", 32),
      fill = (255, 255, 255)
   )
   # ID
   editor.text((748, 62),
      str(user.getID()),
      font = truetype("bahnschrift.ttf", 28),
      fill = (255, 255, 255)
   )
   # Status LEDs
   # # in town?
   status = [user.isInCity(), user.isOpen()]
   r_ = 28
   pointYs = [132, 208]
   for i in range(len(status)):
      x = 985
      y = pointYs[i]
      color = (255, 0, 0)
      if status[i]:
         color = (0, 255, 0)
      editor.ellipse(
         [(x, y), (x + r_, y + r_)],
         fill = color
      )
   # top floor
   top = "F" + str(user.getTopFloor())
   editor.text(
      (985, 282),
      top,
      font = truetype("bahnschrift.ttf", 32),
      fill = (0, 0, 0)
   )
   # HERO ATTRIBUTES: NEEDS TO CHECK FOR HERO
   hero = user.getHero()
   if hero != None:
      # level background
      lvlBox = Image.new("RGBA", (52, 50),(128, 128, 128, 80))
      base.paste(lvlBox, (51, 101), lvlBox)
      # level
      level = str(hero.getLevel().getCurrent())
      myFont = truetype("bahnschrift.ttf", 46)
      posX = 75 - int(myFont.getlength(level) / 2) # center in lvlbox
      editor.text(
         (posX, 103), 
         level,
         font = myFont,
         fill = (0, 0, 0)
      )
      # class description
      lore = hero.getLore()
      myFont = truetype("bahnschrift.ttf", 28)
      adjusted = str()
      line = str()
      for w in lore.split(): # adjust to space
         line += w + ' '
         if not (myFont.getlength(line) < 640): # overflows the line
            word = None
            if myFont.getlength(line) > 660: # too big
               line = line.split()
               word = line[-1]
               line = line[:-1]
               line = ' '.join(line)
            adjusted += line + '\n' # add a new line
            line = str() # clear line
            if word != None:
               line += word + ' ' # add overflowing word
      adjusted += line # add last line
      editor.text((276, 180),
         adjusted,
         font = myFont,
         fill = (255, 255, 255)
      )
      # stats
      uStats = hero.getStats() # unit stats collection
      posYs = [375, 405, 435, 470, 505, 540, 572]
      allStats = uStats.getFullStats()
      myFont = truetype("bahnschrift.ttf", 24)
      for i in range(len(allStats)):
         posX = 345
         stat = str()
         if STATS[i] == "health":
            cur = uStats.getStat("health").getCurrent()
            full = uStats.getStat("health").getFull()
            color = tuple()
            if cur < (.25 * full): # less than 25%
               color = (255, 0, 0)
            elif cur < (.5 * full): # less than 50%
               color = (255, 255, 0)
            else: # over 50%
               color = (0, 255, 0)
            stat = str(cur) + " / " + str(full)
         else: # other stats
            stat = str(uStats.getStat(STATS[i]).getFull())
            color = (255, 255, 255)
         posX -= int(myFont.getlength(stat))
         editor.text(
            (posX, posYs[i]),
            stat,
            font = myFont,
            fill = color
         )
      # equipment pictures
      gear = list()
      gear.append(hero.getEquipped().getWeapon())
      gear.append(hero.getEquipped().getArmour())
      gear.append(hero.getEquipped().getAccessory())
      posYs = [403, 470, 537]
      for i in range(len(gear)):
         if gear[i] != None:
            gear[i] = gear[i].getIco() # get paths to pics
            if gear[i] != '':
               gear[i] = Image.open(gear[i]) # load icon
               gear[i] = gear[i].copy() # duplicate
               gear[i] = gear[i].resize((50, 50)) # resize
               base.paste(gear[i], (407, posYs[i])) # paste
      # equipment names
      gear = list()
      gear.append(hero.getEquipped().getWeapon())
      gear.append(hero.getEquipped().getArmour())
      gear.append(hero.getEquipped().getAccessory())
      posYs = [425, 490, 560]
      for i in range(len(gear)):
         if gear[i] != None:
            gear[i] = gear[i].getName() # recover name
            editor.text(
               (470, posYs[i]), 
               gear[i],
               font = truetype("bahnschrift.ttf", 28),
               fill = (0, 0, 0)
            )
      # skill names
      skills = list()
      skills.append(hero.getSkillSet().getSkill("base"))
      skills.append(hero.getSkillSet().getSkill("ability"))
      skills.append(hero.getSkillSet().getSkill("reaction"))
      skills.append(hero.getSkillSet().getSkill("critical"))
      posYs = [400, 452, 510, 570]
      for i in range(len(skills)):
         if skills[i] != None:
            skills[i] = skills[i].getName() # recover name
            editor.text(
               (750, posYs[i]), 
               skills[i],
               font = truetype("bahnschrift.ttf", 26),
               fill = (255, 255, 255)
            )
      # end of hero attributes
   # send out
   # base.show()
   outputName = OUTPUT + "p_{}".format(user.id) + ".png"
   base.save(outputName)
   return outputName

# inventory
def genBag(user: IdleUser) -> str:
   '''loads a picture that represents the bag of an player.
   place the items in the bag of the adventurer on the picture
   generating an accurate picture of it. return the path
   to the picture.'''
   # set up
   base = Image.open(PAGES + BAG) # load original picture
   base = base.copy() # make copy to not lose base
   editor = Draw(base) # make drawing context on base
   # money
   if user.hasHero():
      cash = str(user.getHero().getWallet().getBalance()) + " gold"
      editor.text(
         (400, 52),
         cash,
         font = truetype("bahnschrift.ttf", 28),
         fill = (0, 0, 0)
      )
   # items positions
   row = 0
   col = 0
   iconsXs = [47, 300, 545, 805]
   iconsY = 110
   namesXs = [112, 365, 616, 860]
   namesY = 145
   # load bag
   bag = user.getHero().getBag()
   # place items
   for i, stack in enumerate(bag):
      # change row, col
      if (i + 1) > 23: # 4rth row
         row = 1
         col = i % 8
      elif (i + 1) > 15: # 3rd row
         row = 2
         col = i % 16
      elif (i + 1) > 7: # 2nd row
         row = 3
         col = i % 24
      else: # first row
         row = 0
         col = i      
      # icons
      ico = stack[0].getIco()
      if ico == '': # there is no set icon
         ico = DEFAULT
      ico = Image.open(ico) # load icon
      ico = ico.copy() # duplicate
      ico = ico.resize((55, 53)) # resize
      x, y = iconsXs[row], iconsY  + col * 65
      base.paste(ico, (x, y)) # paste
      # qty box
      qtyBox = Image.new("RGBA", (16, 16),(255, 255, 255, 180))
      base.paste(qtyBox, (x - 3, y - 2), qtyBox)
      # qty
      qty = str(len(stack))
      myFont = truetype("bahnschrift.ttf", 16)
      posX = (x + 5) - int(myFont.getlength(qty) / 2) # center
      editor.text(
         (posX, y),
         qty,
         font = myFont,
         fill = (0, 0, 0)
      )
      # names
      qty = stack[0].getName()
      myFont = truetype("bahnschrift.ttf", 16)
      editor.text(
         (namesXs[row], namesY + col * 65),
         qty,
         font = myFont,
         fill = (255, 255, 255)
      )
   # send out
   outputName = OUTPUT + "b_{}".format(user.id) + ".png"
   base.save(outputName)
   return outputName
   
# item
def genItem(user: IdleUser, itemName: str) -> str:
   '''upgrade a picture into showing details about an item 
   owned by the passed user.'''
   # set up
   base = Image.open(PAGES + ITEM) # load original picture
   base = base.copy() # make copy to not lose base
   editor = Draw(base) # make drawing context on base
   # take out the item for processing
   bag = user.getHero().getBag()
   item = bag.takeOut(itemName)[0] # get rid of list
   # icon
   ico = item.getIco()
   if ico == '': # there is no set icon
      ico = DEFAULT
   ico = Image.open(ico) # load icon
   ico = ico.copy() # duplicate
   ico = ico.resize((55, 53)) # resize
   base.paste(ico, (8, 8)) # paste
   # name
   name = item.getName()
   editor.text(
      (70, 25),
      name,
      font = truetype("bahnschrift.ttf", 32),
      fill = (255, 255, 255)
   )
   # lore
   lore = item.getLore()
   # add characteristics if gear
   if isinstance(item, Gear):
      # recover line about characteristics
      descr = item.__str__()
      lore += ' ' + descr.split('\n')[-1] 
   myFont = truetype("bahnschrift.ttf", 25)
   adjusted = str()
   line = str()
   for w in lore.split(): # adjust to space
      line += w + ' '
      if not (myFont.getlength(line) < 250): # overflows the line
         word = None
         if myFont.getlength(line) > 270: # too big
            line = line.split()
            word = line[-1]
            line = line[:-1]
            line = ' '.join(line)
         adjusted += line + '\n' # add a new line
         line = str() # clear line
         if word != None:
            line += word + ' ' # add overflowing word
   adjusted += line # add last line
   # write on pic
   editor.text(
      (15, 70),
      adjusted,
      font = myFont,
      fill = (255, 255, 255)
   )
   # value
   plural = item.getValue() > 1
   value = str(item.getValue()) + " gold"
   if plural:
      value += 's'
   editor.text(
      (90, 255),
      value,
      font = truetype("bahnschrift.ttf", 28),
      fill = (255, 255, 255)
   )
   # put the item back in bag
   bag.add(item)
   
   # send out
   outputName = OUTPUT + "i_{}".format(user.id) + ".png"
   base.save(outputName)
   return outputName