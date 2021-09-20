# testing imports
import confrontation as cf
import skillLib as skl
import classes as c
import monsterLib as ml
from sys import exit
from icecream import IceCreamDebugger

if __name__ == "__main__":
   dbg = IceCreamDebugger()
   
   '''myLewysG = c.Fighter("myLewysG")
   myLewysG.getSkillSet().assign("ability", skl.comboAttack)
   myLewysG.getSkillSet().assign("reaction", skl.counter)
   myLewysG.getSkillSet().assign("critical", skl.braceForImpact)
   '''
   
   '''myLewysG = c.Ranger("myLewysG")
   myLewysG.getSkillSet().assign("ability", skl.takeAim)
   myLewysG.getSkillSet().assign("reaction", skl.footwork)
   myLewysG.getSkillSet().assign("critical", skl.firstAid)
   '''
   
   myLewysG = c.Elementalist("myLewysG")
   myLewysG.getSkillSet().assign("ability", skl.embers)
   myLewysG.getSkillSet().assign("reaction", skl.weaken)
   myLewysG.getSkillSet().assign("critical", skl.cure)
   
   p = cf.Party([myLewysG])
   p2 = cf.Party([ml.s_Raccoundrel(), ml.s_Raccoundrel(), 
      ml.s_Raccoundrel()])
   bState = cf.BattleState(p, p2)
   if bState.run() == p: # adventurer(s) won
      bState.awardExp()
      bState.collectLoot()
      bState.recoverLostItems()
   dbg(myLewysG.getBag().__str__())