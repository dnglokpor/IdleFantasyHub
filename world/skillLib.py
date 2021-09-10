'''
# skillLib.py
# this module contains predefined skills and function
# that they use that can be imported and added to 
# characters.
# date: 7/4/21
# author: dnglokpor
'''

# imports
from base import STATS, Cooldown
from elements import Element, NOELM, AEOLA, GAIA, AQUA,\
VULCAN
from skills import Skill, Effect, Mastery
from units import Unit
from confrontation import BattleState
from collectibles import Sword, Spear, Bow, Artillery,\
Staff, Tome
from random import seed, choice
from math import floor
from icecream import IceCreamDebugger

# helpers
dbg = IceCreamDebugger()
seed() # seeding rnd gen
def chance(chances: int) -> bool:
   '''return "True" if a randomly choosen number between
   0 and 99 is lower than "chances".'''
   return choice(range(100)) <= chances
def hasWeapon(unit):
   '''return True if the unit weapon slot is not empty.'''
   return unit.getEquipped().getGear("WPN") != None
def hasWeaponType(wType: str, unit: Unit):
   '''return "True" if the unit's weapon is of specified
   type.'''
   weapon = unit.getEquipped().getGear("WPN")
   hasIt = bool()
   if weapon != None:
      if wType == 'b': # bladed
         hasIt = isinstance(weapon, (Sword, Spear))
      elif wType == 'r': # ranged
         hasIt = isinstance(weapon, (Bow, Artillery))
      elif wType == 'm': # magic
         hasIt = isinstance(weapon, (Staff, Tome))
      else: # wrong keyword thus default to False
         hasIt = False
   return hasIt
def singleTarget(perp: Unit, state):
   '''returns a target for a single target attack.'''
   return state.getOpponents(perp).getWeakestMember()
def restartCooldown(skill: Skill):
   '''restart cooldown for the skill if the skill elapsed
   cooldown is not 0.'''
   # restart cooldown
   if skill.cd.getElapsed() != 0:
      skill.cd.reset() 
def targetAttack(perp: Unit, target: Unit, ofs: int, 
   elt, dmgMult = 1.0) -> str:
   '''deals STATS[offense] damage to one opponent defending
   with a stat selected based on the offense stat. the normal
   damage is multiplied by multiplier before critical or
   resistance computations. a tuple specifying which unit
   was hit or missed and the desciption of the events.
   '''
   descr = None
   # target has dext chances to avoid the hit 
   if chance(target.getStats().getStat("dexterity").getCurrent()):
      # the target avoided the attack
      hit = "missed {}!".format(target.getName())
      descr = (None, hit)
   else: # target was hit
      hit = "dmg to {}"
      # compute potential damage
      dmg = perp.getStats().getStat(ofs).getCurrent()
      dmg *= dmgMult
      dmg = floor(dmg) # keep it int
      # elemental boost
      if elt > target.getElement():
         dmg *= 4 # quadruple potential damage
      elif elt < target.getElement():
         dmg //= 2 # half potential damage
      elif elt != NOELM and elt == target.getElement():
            dmg = 0  # immunity
      else: # no elemental bonus
         pass
      # perp has 5 + luck chances to deal crit damage
      if chance(perp.getStats().getStat("luck").getCurrent()):
         dmg *= 2 # critical hit so double dmg
         hit = "crit. " + hit
      # substract target's defense
      dfs = "defense"
      if ofs == "special":
         dfs = "resilience"
      dmg -= target.getStats().getStat(dfs).getCurrent()
      if dmg < 0: 
         dmg = 0 # can only deal positive damage (>= 0)
      # inflict damage
      target.suffer(dmg)
      hit = "dealt {} hp " + hit
      hit = hit.format(dmg, target.getName())
      if not target.isAlive():
         hit += "\n{} died!".format(target.getName())
      descr = (target, hit)
   # return outcome message
   return descr
def raiseStat(unit, sName, mult) -> str:
   '''raise a stat by its full value times the multiplier.
   the value of buff decides if its a buff or a debuff. 
   default to a buff.'''
   old = unit.stats.getStat(sName).getFull()
   value = floor(old * mult)
   unit.stats.changeBy(sName, value)
   return value
def lowerStat(unit, sName, mult) -> str:
   '''reduce a stat by its full value times the multiplier.
   the value of buff decides if its a buff or a debuff. 
   default to a buff.'''
   old = unit.stats.getStat(sName).getFull()
   value = floor(old * mult)
   unit.stats.changeBy(sName, -value)
   return value

##########################SKILLS LIBRARY#########################

################## skill subclasses
# single physical attacks
class SinglePhysical(Skill):
   '''define basic physical attacks on a single target.'''
   def __init__(self, name: str, descr: str, cd: int,
      power = 1.0, elt = NOELM):
      super().__init__(name, descr, cd, elt, power)
   
   # action override
   def __call__(self, perp: Unit, state):
      '''executes the attack.'''
      target = singleTarget(perp, state)
      restartCooldown(self)
      return targetAttack(perp, target, "attack", 
         self.element, self.power)

# single special attacks
class SingleSpecial(Skill):
   '''define basic special attacks on a single target.'''
   def __init__(self, name: str, descr: str, cd: int,
      power = 1.0, elt = NOELM):
      super().__init__(name, descr, cd, elt, power)
   
   # action override
   def __call__(self, perp: Unit, state):
      '''executes the attack.'''
      target = singleTarget(perp, state)
      # restart cooldown
      restartCooldown(self)
      return targetAttack(perp, target, "special", 
         self.element, self.power)

# stat buff skill
class Buff(Skill):
   '''define a skill that raise a list of stats for the
   perpetrator.'''
   def __init__(self, name: list, descr: str, cd: int,
      stat: str, dur = 3, power = 0.25):
      super().__init__(name, descr, cd, NOELM, power)
      self.raised = stat
      self.dur = dur
   
   def __call__(self, perp, state):
      '''implement the buffing.'''
      txt = str()
      for stat in self.raised:
         # create effect
         buff = Effect(self.dur, stat, raiseStat, self.power)
         # add to active effects
         perp.getActiveEffects().addEffect(buff)
         # activate effect immediatly and return status
         txt += "raised {}'s {} by {}! ".format(perp.getName(),
            stat, buff(perp))
      restartCooldown(self)
      # return status
      return (None, txt)

# stat buff skill
class Debuff(Skill):
   '''define a skill that reduces a list of stats for
   a target.'''
   def __init__(self, name: list, descr: str, cd: int,
      stat: str, dur = 3, power = 0.25):
      super().__init__(name, descr, cd, NOELM, power)
      self.raised = stat
      self.dur = dur
   
   def __call__(self, perp, state):
      '''implement the debuffing.'''
      txt = str()
      target = singleTarget(perp, state)
      for stat in self.raised:
         # create effect
         buff = Effect(self.dur, stat, lowerStat, self.power)
         # add to active effects
         target.getActiveEffects().addEffect(buff)
         # activate effect immediatly and return status
         txt += "reduced {}'s {} by {}! ".format(target.getName(),
            stat, buff(perp))
      restartCooldown(self)
      # return status
      return (target, txt)

# single target magic attack
class Magic(SingleSpecial):
   '''magic is a skill that some adventurers can conjure. magic
   requires a magic weapon thus the weapon type will be
   checked on each magic skill.'''
   def __init__(self, name: str, descr: str, cd: int,
      power = 1.0, elt = NOELM):
      super().__init__(name, descr, cd, power, elt)
   
   # action override
   def __call__(self, perp: Unit, state):
      '''implement the magic. test for a magic weapon first.'''
      status = None
      # check for a magic weapon
      if hasWeaponType('m', perp):
         status = super().__call__(perp, state)
      else: # had no magic weapon so it is a miss
         status = (None, "{} can't cast magic!".format(
         perp.getName()))
         self.cd.reset() # restart cooldown
      return status

################## monsters
# Sting
sting = SinglePhysical(
   "Sting", 
   "stabs the target with a sturdy painfully sharp stinger.",
   0, 
   1.0, 
   NOELM
)
# Bite
bite = SinglePhysical(
   "Bite",
   "chomp off a piece of the target flesh.",
   0, 
   1.0,
   NOELM
)
# Charge
charge = SinglePhysical(
   "Charge",
   "ram into the target with a full body tackle.",
   0,
   1.0,
   NOELM
)
# Peck
peck = SinglePhysical(
   "Peck",
   "a painful peck inflicted by a hard beak.",
   0,
   1.0,
   NOELM
)
# Scratch
scratch = SinglePhysical(
   "Scratch",
   "inflit a stripes-like wound with razor sharp claws.",
   0,
   1.0,
   NOELM
)
# Whoosh
whoosh = SingleSpecial(
   "Whoosh",
   "hit a target a pressurized burst of wind.",
   3,
   1.0,
   AEOLA
)

################## blademanship
# Strike
class Strike(SinglePhysical):
   '''single physical attack on a single target that requires
   the perpetrator to have a weapon.'''
   def __init__(self):
      super().__init__(
         "Strike", 
         "strike the target with the weapon in hand. fails\
 if there are no weapons in hand.",
         0, 
         1.0,
         NOELM
      )
   
   # action override
   def __call__(self, perp: Unit, state):
      '''executes the attack. first check that the perpetrator
      has any weapon on them.'''
      status = None
      if hasWeapon(perp):
         status = super().__call__(perp, state)
      else: # had no weapon so we count it as a miss
         status = (None, "{} has no weapon.".format(
         perp.getName()))
         restartCooldown(self)
      return status
strike = Strike()

# Fighting Stance
fightingStance = Buff(
   "Fighting Stance",
   "takes a battle stance that slightly increase offensive\
 capabilities for 3 turns.",
   3,
   ["attack",],
   4,
   0.50
)

# Counter
class Counter(SinglePhysical):
   '''single physical attack back to a unit that just
   attacked the perpetrator first.'''
   def __init__(self):
      super().__init__(
         "Counter",
         "strike back at a the foe who just striked at you.\
 fails if not used as a reaction.",
         4,
         1.5,
         NOELM  
      )
   
   # action override
   def __call__(self, perp: Unit, state):
      '''execute the counter. this test that the perpetrator
      is not the unit's whose turn it is before doing the
      attack.'''
      status = None
      target = state.isMoving()
      # check for reaction move
      if perp != target: 
         txt = "{} attacks {} back!".format(perp.getName(),
            target.getName())
         status = super().__call__(perp, state)
         status = (status[0], txt + '\n' + status[1])
      else:
         status = (None, "counter failed!")
      # reset CD
      restartCooldown(self)
      return status
counter = Counter()

# Brace For Impact
braceForImpact = Buff(
   "Brace For Impact",
   "raise defense and resilience for 3 turns to prepare\
 for incoming hits.",
   3,
   ["defense", "resilience"],
   4,
   0.25
)

# Combo Attack
class ComboAttack(SinglePhysical):
   '''performs a series of single physical attacks on
   a single target. max number of attacks: 5'''
   def __init__(self):
      super().__init__(
         "Combo Attack",
         "Attacks a single opponent with a series of up to"
         "5 successive attacks. the streak stops if you"
         "miss a hit or if the target dies.",
         7,
         1.0,
         NOELM  
      )
      
   # action override
   def __call__(self, perp: Unit, state):
      '''implement the combo attack skill.'''
      failed = False
      i = 0
      status = list()
      # combo loop
      while i < 5 and not failed:
         returned = super().__call__(perp, state)
         # if the attack missed or the target died, stop
         failed = (returned[0] == None or\
            not returned[0].isAlive())
         # update status
         status.append(returned)
         # set next attack
         if not failed:
            i += 1
      # return
      return status
comboAttack = ComboAttack()

################## survivalist
# shoot
class Shoot(SinglePhysical):
   '''performs a single physical attack on a single target
   but only if the perpetrator has a ranged weapon.'''
   def __init__(self):
      super().__init__(
         "Shoot",
         "shoot an arrow or a bullet at a target with a ranged"
         " weapon. requires projectiles.",
         0,
         1.0,
         NOELM  
      )
   
   # action override
   def __call__(self, perp: Unit, state):
      '''implement the shoot. test for a ranged weapon first.'''
      status = None
      # check for a ranged weapon
      if hasWeaponType('r', perp):
         # check for ammo
         ammo = perp.getBag().takeOut("arrow")
         if len(ammo) != 0:
            status = super().__call__(perp, state)
            # add ammo to waste
            state.addLostItem(perp, ammo[0])
         else: # no arrows
            status = (None, "{} has no arrows.".format(
         perp.getName()))
      else: # had no ranged weapon so it is a miss
         status = (None, "{} has nothing to shoot with.".format(
         perp.getName()))
         self.cd.reset() # restart cooldown
      return status
shoot = Shoot()

# take aim
class TakeAim(Buff):
   '''raise attack for the next turn. require a ranged weapon.'''
   def __init__(self):
      super().__init__(
         "Take Aim",
         "aim its ranged weapon to get an attack boost the next"
         " turn. requires a bow.",
         3,
         ["attack",],
         2,
         0.50
      )
   
   # action override
   def __call__(self, perp: Unit, state):
      '''implement take aim. test for a ranged weapon first.'''
      status = None
      # check for a ranged weapon
      if hasWeaponType('r', perp):
         status = super().__call__(perp, state)
      else: # had no ranged weapon so it is a miss
         status = (None, "{} has nothing to aim with.".format(
         perp.getName()))
         self.cd.reset() # restart cooldown
      return status
takeAim = TakeAim()

# footwork
footwork = Buff(
   "Footwork",
   "Use agile footwork around the field to raise dexterity.",
   5,
   ["dexterity",],
   3,
   0.25
)

# first aid
firstAid = Buff(
   "First Aid",
   "use therapeutic knowledge to patch up wounds and recover"
   " some health.",
   7,
   ["health",],
   0,
   0.25
)

# tri-shot
class TriShot(Shoot):
   '''attacks three times in a row with a ranged weapon.
   targets can be different each time.'''
   def __init__(self):
      super().__init__()
      # update attributes
      self.name = "Tri-Shot",
      self.description = "attacks opposing party three times with\
 a ranged weapon."
      self.cd = Cooldown(6)
      self.element = NOELM  
      self.power = 1.0
   
   # action override
   def __call__(self, perp: Unit, state):
      '''implement the tri-shot attack skill.'''
      failed = False
      i = 0
      targets = list
      txt = str()
      # combo loop
      while i < 3 and not failed:
         returned = super().__call__(perp, state)
         # stop if battle ended after a shot
         failed = state.isOver()
         # update status
         targets.append(returned[0])
         txt += returned[1]
         # set next attack
         if not failed:
            i += 1
            status += '\n'
      # return
      if i == 0: # no attack was successful
         status = (None, status)
      else:
         status = (targets, status)
      return status
triShot = TriShot()

################## conjuring
manaStrike = Magic(
   "Mana Strike",
   "create a mana disturbance that inflicts raw magic"
   " damage to one opponent.",
   0,
   1.0,
   NOELM
   
)
gust = Magic(
   "Gust",
   "conjure and blows a target with a scathing gust of"
   " wind.",
   4,
   1.5,
   AEOLA  
)

# stone sling
stoneSling = Magic(
   "Stone Sling",
   "conjure a small pointy roc and hurl it at the target.",
   4,
   1.5,
   GAIA
)

# water whip
waterWhip = Magic(
   "Water Whip",
   "conjure a semi rigid stream of water to whip a target.",
   4, 
   1.5, 
   AQUA
)

# embers
embers = Magic(
   "Embers",
   "conjure and throw at a target burning hot fiery sparks.",
   4, 
   1.5, 
   VULCAN
)

# weaken
weaken = Debuff(
   "Weaken",
   "conjure up a cloud of magic that impairs the ability"
   " of the target to muster its strength. reduces attack.",
   5,
   ["attack",],
   0,
   0.25
)
   

# magic shield
class MagicShield(Buff):
   '''magic skill that raise defense by 25% for 3 turns.'''
   def __init__(self):
      super().__init__(
         "Magic Shield",
         "conjures an air barrier that reduces physical damages\
 taken.",
         4,
         ["defense",],
         3,
         1.25
      )
   
   # action override
   def __call__(self, perp: Unit, state):
      '''implement take aim. test for a magic weapon first.'''
      status = None
      # check for a magic weapon
      if hasWeaponType('m', perp):
         status = super().__call__(perp, state)
      else: # had no ranged weapon so it is a miss
         status = (None, "{} can't cast magic!".format(
         perp.getName()))
         self.cd.reset() # restart cooldown
      return status
magicShield = MagicShield()

# cure 
class Cure(Buff):
   '''magic skill that heals 40% of perpetrator HP.'''
   def __init__(self):
      super().__init__(
         "Cure",
         "heals some hp using magic to hasten body regen.",
         5,
         ["health",],
         0,
         1.40
      )
   
   # action override
   def __call__(self, perp: Unit, state):
      '''implement cure. test for a magic weapon first.'''
      status = None
      # check for a magic weapon
      if hasWeaponType('m', perp):
         status = super().__call__(perp, state)
      else: # had no ranged weapon so it is a miss
         status = (None, "{} can't cast magic!".format(
         perp.getName()))
         self.cd.reset() # restart cooldown
      return status
cure = Cure()

# Masteries library
blademanship = Mastery("Blademanship",
   "collection of skills for the blade afficionado.",
   [(1, strike), (3, braceForImpact), (7, counter), 
      (10, fightingStance), (20, comboAttack),
   ]
)
survivalist = Mastery("Survivalist",
   "techniques prized by the ones unfazed by the wilderness.",
   [(1, shoot), (3, takeAim), (7, footwork), (10, firstAid),
      (20, triShot),
   ]
)
conjuring = Mastery("Conjuring",
   "spells at the service of those who have the ability to\
 wield them.",
   [(1, manaStrike), (3, magicShield), (7, cure),
      (10, weaken), (20, embers)
   ]
)