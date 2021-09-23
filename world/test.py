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
   
   '''p2 = cf.Party([ml.s_Raccoundrel(), ml.s_Raccoundrel(), 
      ml.s_Raccoundrel()])
   bState = cf.BattleState(p, p2)
   bState.run()
   dbg(myLewysG.getBag().__str__())
   '''
   
   # Blocks
   import blocks as bk
   import itemLib as il
   '''eEnv = bk.Environment(1, 
      ["There is lush green tall grass all around the place.",
       "The wind blows slowly among the small bushes.",
       "Bugs can be heard chirping gladly in the sunlight."
      ],
      res = None,
      hostile = None, 
      amenity = None
   )
   eBlock = bk.EmptyBlock(eEnv)
   #print(eBlock)
   eBlock.explore(p)
   '''
   sEnv = bk.Environment(1, 
      look = 
      ["the prairie seems ripe with fragrant plants and flowers.",
       "herb picking would definitely yield results.",
      ],
      res = [il.chemomille, il.dandetigerSeeds, il.theestleNeedles],
      hostile = [ml.s_Sparowl],
      amenity = None
   )
   sBlock = bk.ScavengingBlock(sEnv)
   #print(eBlock)
   sBlock.explore(p)
   