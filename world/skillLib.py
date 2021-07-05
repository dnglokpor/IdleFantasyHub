'''
# skillLib.py
# this module contains predefined skills and function
# that they use that can be imported and added to 
# characters.
# date: 7/4/21
# author: dnglokpor
'''

# imports
from base import STATS
from elements import Element, NOELM, AEOLA, GAIA, AQUA,\
VULCAN
from skills import Skill, Effect
from units import Unit
from confrontation import BattleState
from collectibles import Sword, Spear, Bow, Artillery,\
Staff, Tome
from random import choice
from math import floor

# helpers
def chance(luckStat: int) -> bool:
   '''return "True" if a randomly choosen number between
   0 and 99 is lower than the luck stat passed.'''
  return choice(range(100)) <= perp.getStats().getStat(STATS[4])
def hasWeaponType(wType: str, unit: Unit):
   '''return "True" if the unit's weapon is of specified
   type.'''
   weapon = unit.getEquipped().getGear("WPN")
   if wType == 'b': # bladed
      return isinstance(weapon, (Sword, Spear))
   elif wType == 'r': # ranged
      return isinstance(weapon, (Bow, Artillery))
   else: # default to wType == "m"
      return isinstance(weapon, (Staff, Tome))
   
# skills methods
# overall
# offensive move
def attack(perp: Unit, state: BattleState, elt: Element,
   offense: int, defense: int, dmgMult 1.0) -> list:
   '''deals STATS[offense] damage to one opponent defending
   with STATS[defense]. the normal damage is multiplied
   by multiplier before critical or resistance computations.
   '''
   # select target
   target = list()
   target = state.getOpponents(perp).getWeakestMember()
   # check hit
   hit = str()
   if chance(target.getStats().getStat(STATS[4]) + 15):
      hit += "miss" # the target avoided the attack
   else:
      hit += "hit"
      # compute damage starting with perp's offense
      dmg = perp.getStats().getStat(STATS[offense])
      dmg *= dmgMult
      dmg = floor(dmg)
      # elemental boost
      if elt > target.getElement():
         dmg *= 4 # quadruple the attack power
      elif elt < target.getElement():
         dmg //= 2 # half attack power
      else: # same element 
         if elt != NOELM: # immunity
         dmg = 0
      # substract target's defense to get damage
      dmg -= target.getStats().getStat(STATS[defense])
      if dmg < 0: 
         dmg = 0 # can only deal positive damage (>= 0)
      # STATS[4] == "luck"
      if chance(perp.getStats().getStat(STATS[4])):
         hit = "crit"
         dmg *= 2 # critical hit so double dmg
      # inflict damage
      target.getStats().inflict(-dmg)
   # return the hit status and target
   return [(hit, target),]

# basic physical attack
def physical(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None) -> list:
   '''"perp" picks a target in the other party
   and attack them. damage inflicted depends on the
   difference between the perp's attack and the
   target's defense. there is a chance of missing,
   a chance of dealing critical damage. elements of 
   the skill and the target will react to each other
   causing either extra damage, resistance or immunity.'''
   
   return attack(perp, state, elt, 1, 2, dmgMult)

# basic bladed weapon required
def bladedRequired(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None) -> list:
   '''calls the basic physical attack only if the perp
   has a sword or a spear.'''
   target = list()
   if hasWeaponType('b', perp):
      target = physical(perp, state, elt, dmgMult)
   return target

# basic ranged weapon required
def rangedRequired(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None) -> list:
   '''calls the basic physical attack only if the perp
   has a bow or an artillery.'''
   target = list()
   if hasWeaponType('r', perp):
      # TBD make it so you use up projectiles to shoot
      target = physical(perp, state, elt, dmgMult)
   return target 

# basic special attack
def special(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None) -> list:
   '''similar to "attack" but uses "special" stat for
   offense and "resilience" for defense.'''
   
   return attack(perp, state, elt, 3, 4, dmgMult)

# basic magic weapon required
def magicRequired(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None) -> list:
   '''calls the basic special attack only if the perp
   has a staff or a tome.'''
   target = list()
   if hasWeaponType('m', perp):
      target = special(perp, state, elt, dmgMult, oppressor)
   return target

# buff effect function
def selfBuff(perp: Unit, statsList: list,
   dur: int, mult = 1.25,) -> list:
   '''raises the current value of all the stats specified.
   also creates an Effect and add it to the effects list
   of the unit. last 3 turns.'''
   for stat in statsList:
      old = perp.getStats().getStat(stat).getFull()
      perp.getStats.setStat(stat, floor(mult * old))

# buff wrappers
def raiseAtk(perp: Unit, state: BattleState, elt: Element,
   mult = 1.25, oppressor = None) -> list:
   '''spawn an effect that raise the attack for 3 turns.'''
   e = Effect(3, [STATS[1],], selfBuff, mult)
   perp.getActiveEffects().addEffect(e)
   # apply effect immediatly
   e(perp, e.impacted, e.dur, e.power)
   return [("hit", perp),]
def rr_raiseAtk(perp: Unit, state: BattleState, elt: Element,
   mult = 1.25, oppressor = None) -> list:
   '''spawn an effect that raise the attack for 2 turns.'''
   if not hasWeaponType('r', perp):
      return [("miss", perp),]
   else:
      e = Effect(2, [STATS[1],], selfBuff, mult)
      perp.getActiveEffects().addEffect(e)
      # apply effect immediatly
      e(perp, e.impacted, e.dur, e.power)
      return [("hit", perp),]
def raiseDefs(perp: Unit, state: BattleState, elt: Element,
   mult = 1.25, oppressor = None) -> list:
   '''spawn an effect that raise both the defense and
   the resilience for 3 turns.'''
   e = Effect(3, [STATS[2], STATS[4]], selfBuff, mult)
   perp.getActiveEffects().addEffect(e)
   # apply effect immediatly
   e(perp, e.impacted, e.dur, e.power)
   return [("hit", perp),]
def mr_raiseDef(perp: Unit, state: BattleState, elt: Element,
   mult = 1.25, oppressor = None) -> list:
   '''spawn an effect that raise the defense for 3 turns
   if an only if the user has a magic weapon.'''
   if not hasWeaponType('m', perp):
      return [("miss", perp),]
   else:
      e = Effect(3, [STATS[2]], selfBuff, mult)
      perp.getActiveEffects().addEffect(e)
      # apply effect immediatly
      e(perp, e.impacted, e.dur, e.power)
      return [("hit", perp),]
def raiseDext(perp: Unit, state: BattleState, elt: Element,
   mult = 1.25, oppressor = None) -> list:
   '''spawn an effect that raise the dexterity for 3 turns.'''
   e = Effect(3, [STATS[5],], selfBuff, mult)
   perp.getActiveEffects().addEffect(e)
   # apply effect immediatly
   e(perp, e.impacted, e.dur, e.power)
   return [("hit", perp),]

# counter
def counter(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None):
   '''if oppressor is defined, attacks them.'''
   # check hit
   if oppressor != None: # there is an oppressor
      target = oppressor
      hit = str()
      if chance(target.getStats().getStat(STATS[4]) + 15):
         hit += "miss" # the target avoided the attack
      else:
         hit += "hit"
         # compute damage starting with perp's offense
         dmg = perp.getStats().getStat(STATS[offense])
         dmg *= dmgMult
         dmg = floor(dmg)
         # elemental boost
         if elt > target.getElement():
            dmg *= 4 # quadruple the attack power
         elif elt < target.getElement():
            dmg //= 2 # half attack power
         else: # same element 
            if elt != NOELM: # immunity
            dmg = 0
         # substract target's defense to get damage
         dmg -= target.getStats().getStat(STATS[defense])
         if dmg < 0: 
            dmg = 0 # can only deal positive damage (>= 0)
         # STATS[4] == "luck"
         if chance(perp.getStats().getStat(STATS[4])):
            hit = "crit"
            dmg *= 2 # critical hit so double dmg
         # inflict damage
         target.getStats().inflict(-dmg)
      # return the hit status and target
      return [(hit, target),]
   else:
      return[("miss", None),]

# combo attacks
def physicalCombo(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None):
   '''attacks up 1 to 5 times. extends the list of 
   victims each time.'''
   targets = list()
   acc = 100
   end = False
   while acc > 50 and not end:
      end = choice(100) <= acc
      if not end:
         t = physical(perp, state, elt, dmgMult)
         if not targets.__contains__(t[0]): # not yet recorded
            targets.append(t[0])
         acc -= 10 # decrease accuracy for next rnd
   return targets

# healing moves
def heal(perp: Unit, state: BattleState, elt: Element,
   mult = 1.0, oppressor = None):
   '''gives some hp back to the perp.'''
   full = perp.getStats().getHealth().getFull()
   perp.getStats().getHealth().setStat(STATS[0], 
      floor(mult * full))
   return [("hit", perp),]
def mr_heal(perp: Unit, state: BattleState, elt: Element,
   mult = 1.0, oppressor = None):
   '''gives some hp back to the perp if and only if they
   have a magic weapon.'''
   if hasWeaponType('m', perp):
      return heal(perp, state, elt, mult)
   else:
      return [("miss", perp),]

# multiple attacks
def rr_physical(perp: Unit, state: BattleState, elt: Element,
   dmgMult = 1.0, oppressor = None):
   '''attacks 3 times. extends the list of victims each time.'''
   targets = list()
   for time in range(3):
      t = physical(perp, state, elt, dmgMult)
      if not targets.__contains__(t[0]): # not yet recorded
         targets.append(t[0])
      acc -= 10 # decrease accuracy for next rnd
   return targets

# skills library
# monsters
sting = Skill("Sting",
   "stabs the target with a sturdy painfully sharp stinger.",
   0, physical
)
bite = Skill("Bite",
   "jump on a target and bite them with small fangs.",
   0, physical
)
charge = Skill("Charge",
   "ram into the target with its full body.",
   0, physical
)
peck = Skill("Peck",
   "a small yet painful peck made by a hard bird beak.",
   0, physical
)
scratch = Skill("Scratch",
   "inflit a clawing wound to the target with sharp claws.",
   0, physical
)

# blademanship
strike = Skill("Strike",
   "strike the target with the weapon in hand.",
   0, bladedRequired
)
fightingStance = Skill("Fighting Stance",
   "takes a battle stance to increase offensive capabilities.",
   4, raiseAtk, 1.25)
counter = Skill("Counter",
   "strike back at a the foe who just striked at you.",
   3, counter, 1.0
)
braceForImpact = Skill("Brace For Impact",
   "raise defense and special defense.", 5, raiseDefs,
   1.25
)
comboAttack = Skill("Combo attack",
   "attacks up 1 to 5 times in a single turn.",
   7, physicalCombo, 1.0
)

# survivalist
shoot = Skill("Shoot",
   "shoot an arrow or a bullet at a target with a ranged \
weapon.",
   0, rangedRequired
)
footwork = Skill("Footwork",
   "start using agile footwork around the field to raise\
 dexterity.", 4, raiseDext, 1.25
)
takeAim = Skill("Take Aim",
   "aim its ranged weapon to get an attack boost the next\
  turn", 5, rr_raiseAttack, 2.0
)
firstAid = Skill("First Aid",
   "use therapeutic knowledge to patch up wounds and recover\
 some health.", 5, heal, 1.25
)
triShot = Skill("Tri-Shot", 
   "attacks three times with a ranged weapon.", 7,
   rr_physical, 1.0
)

# conjuring
gust = Skill("Gust",
   "conjure and blows a target with a scathing gust of wind.",
   2, magicRequired, AEOLA
)
stoneSling = Skill("Stone Sling",
   "conjure a small pointy roc and hurl it at the target.",
   2, magicRequired, GAIA
)
waterWhip = Skill("Water Whip",
   "conjure a semi rigid stream of water to whip a target.",
   2, magicRequired, AQUA
)
sparks = Skill("Sparks",
   "conjure and throw at a target burning hot fiery sparks.",
   2, magicRequired, VULCAN
)
magicShield = Skill("Magic Shield",
   "conjures an air barrier that reduces physical damages\
 taken.", 4, mr_raiseDef
)
cure = Skill("Cure",
   "heals some hp using magic to hasten body regen.", 5,
   mr_heal, 1.25
)  

# Mastery object
class Mastery(dict):
   '''the mastery is a collection of moves that are available
   for an adventurer as he gets stronger in a specific class.
   the key is the level at which the skill is available and
   the skill itself is the value.'''
   
   def __init__(self, name: str, lore: str, allSkills: list):
      '''"allSkills" must be a list of tuples.'''
      super().__init__(allSkills)
      self.name = name
      self.lore = lore
   
   # getters
   def getName(self) -> str:
      '''return the Mastery's name.'''
      return self.name
   def getName(self) -> str:
      '''return the Mastery's lore.'''
      return self.lore
   def getSkill(self, uLevel: int, aLevel: int):
      '''return the skill corresponding at "uLevel" if
      "uLevel" is defined and if "uLevel <= aLevel".
      does not return the base skill.'''
      sk = None
      if self.__contains__(uLevel) and uLevel > 1:
         if uLevel <= aLevel:
            sk = self.get(uLevel)
      return sk
   def getUnlocked(self, currentLevel: int) -> list:
      '''return a list of all the skills that are
      already available at "currentLevel" except for
      the base skill.'''
      unlocked = list()
      for lvl, skill in self.items():
         if 1 < lvl <= currentLevel:
            unlocked.append(skill)
      return unlocked
   
   # Mastery is never set
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = "<{}>: {}".format(self.name, self.lore)
      if not short:
         description += '\n'
         for idx, (lvl, skill) in enumerate(self.items()):
            description += "{:12s} - unlocks @ lvl {:3d}".format(
               skill.getName(), lvl)
            if idx != len(self.items()) - 1:
               description += '\n'
      return description
# Masteries library
blademanship = Mastery("Blademanship",
   "collection of skills for the blade afficionado.",
   [(1, strike), (3, fightingStance), (7, counter), 
      (10, braceForImpact), (15, comboAttack),
   ]
)
survivalist = Mastery("Survivalist",
   "techniques prized by the ones unfazed by the wilderness.",
   [(1, shoot), (3, footwork), (7, takeAim), (10, firstAid),
      (15, triShot),
   ]
)
conjuring = Mastery("Conjuring",
   "spells at the service of those who have the ability to\
 wield them.",
   [(1, gust), (2, stoneSling), (3, waterWhip), (4, sparks),
      (10, magicShield), (15, cure),
   ]
)