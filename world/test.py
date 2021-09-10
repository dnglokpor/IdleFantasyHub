# testing imports
import classes as c
import monsterLib as ml
import confrontation as cf
from sys import exit
from icecream import IceCreamDebugger
try:
   import skillLib as skl
except ImportError:
   pass

if __name__ == "__main__":
   dbg = IceCreamDebugger()
   '''
   #myLewysG = c.Fighter("myLewysG")
   #myLewysG.getSkillSet().assign("ability", skl.comboAttack)
   #myLewysG.getSkillSet().assign("reaction", skl.counter)
   #myLewysG.getSkillSet().assign("critical", skl.braceForImpact)
   '''
   myLewysG = c.Ranger("myLewysG")
   myLewysG.getSkillSet().assign("ability", skl.takeAim)
   myLewysG.getSkillSet().assign("reaction", skl.footwork)
   myLewysG.getSkillSet().assign("critical", skl.firstAid)
   #myLewysG = c.Elementalist("myLewysG")
   p2 = cf.Party([myLewysG])
   p = cf.Party([ml.s_Sparowl(), ml.s_Sparowl()])
   bState = cf.BattleState(p, p2)
   bState.run()
   bState.awardExp()
   bState.collectLoot()
   bState.recoverLostItems()
   dbg(myLewysG.getBag().__str__())