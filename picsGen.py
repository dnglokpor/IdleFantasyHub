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

# constants
PAGES = "world/resource/pages/"
OUTPUT = "records/generated/"
PROFILE = "profile.png"
PP_SIZE = 180

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
   if pp.width > PP_SIZE or pp.height > PP_SIZE: # resize if necessary
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
   status = [user.isInCity(), user.isAvailable()]
   r_ = 28
   pointYs = [182, 262]
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
      editor.text((276, 180),
         lore,
         font = truetype("bahnschrift.ttf", 28),
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
               base.paste(gear[i], (407, posYs[i])) # paste weapon
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
      posYs = [400, 450, 510, 570]
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
   outputName = OUTPUT + "{}".format(user.id) + ".png"
   base.save(outputName)
   return outputName