# testing imports
import confrontation as cf
import skillLib as skl
import classes as c
import monsterLib as ml
import bossLib as bl
from sys import exit
from time import sleep
from icecream import IceCreamDebugger

if __name__ == "__main__":
   dbg = IceCreamDebugger()
   
   myLewysG = c.Fighter("myLewysG")
   myLewysG.getSkillSet().assign("ability", skl.fightingStance)
   myLewysG.getSkillSet().assign("reaction", skl.counter)
   myLewysG.getSkillSet().assign("critical", skl.braceForImpact)
   myLewysG.develup(1000) # levelup to 5
   # print(myLewysG)
   # print(myLewysG.getMastery().__str__(False))
   
   '''myLewysG = c.Ranger("myLewysG")
   myLewysG.getSkillSet().assign("ability", skl.takeAim)
   myLewysG.getSkillSet().assign("reaction", skl.footwork)
   myLewysG.getSkillSet().assign("critical", skl.firstAid)
   '''
   
   '''myLewysG = c.Elementalist("myLewysG")
   myLewysG.getSkillSet().assign("ability", skl.embers)
   myLewysG.getSkillSet().assign("reaction", skl.weaken)
   myLewysG.getSkillSet().assign("critical", skl.cure)
   '''
   
   p = cf.Party([myLewysG])
   print("hero stats:\n", myLewysG.getStats())
   
   '''p2 = cf.Party([ml.s_Raccoundrel(), ml.s_Raccoundrel(), 
      ml.s_Raccoundrel()])
   bState = cf.BattleState(p, p2)
   bState.run()
   dbg(myLewysG.getBag().__str__())
   '''
   
   # Blocks
   import blocks as bk
   import itemLib as il
   '''
   eEnv = bk.Environment( 
      ["There is lush green tall grass all around the place.",
       "The wind blows slowly among the small bushes.",
       "Bugs can be heard chirping gladly in the sunlight."
      ],
      res = None,
      hostile = None, 
      amenity = None
   )
   eBlock = bk.EmptyBlock(eEnv)
   '''
   #print(eBlock)
   #eBlock.explore(p)
   
   '''
   sEnv = bk.Environment(
      look = 
      ["the prairie seems ripe with fragrant plants and flowers.",
       "herb picking would definitely yield results.",
      ],
      res = [il.chemomille, il.dandetigreSeeds, il.theestleNeedles],
      hostile = [ml.s_Sparowl],
      amenity = None
   )
   sBlock = bk.ScavengingBlock(sEnv)
   '''
   #print(sBlock)
   #sBlock.explore(p)
   
   '''bEnv = bk.Environment(
      look = 
      ["a sudden air of danger float around the prairie.",
       "something moves in the grass in front of the party.",
       "weapons in hand you get ready to welcome the monsters..."
      ],
      res = None,
      hostile = [ml.s_Raccoundrel, ml.s_Sparowl],
      amenity = None
   )
   bBlock = bk.BattleBlock(bEnv)
   '''
   #print(bBlock)
   #bBlock.explore(p, 1)
   
   
   '''
   wEnv = bk.Environment( 
      look = 
      ["the trees around here seem to be of good quality.",
       "logging here could turn out profitable.",
      ],
      res = [il.haukWood, il.hardcorn],
      hostile = [ml.s_Honeybeat],
      amenity = None
   )
   wBlock = bk.WoodcuttingBlock(wEnv)
   print(wBlock)
   #myLewysG.getBag().add(il.axe)
   #wBlock.explore(p)
   '''
   
   
   '''mEnv = bk.Environment(
      look = 
      ["the walls of this cave are covered in sparkly materials.",
       "mining here should not be a waste of time.",
      ],
      res = [il.ironOre, il.palemethyst],
      hostile = [ml.s_Raccoundrel],
      amenity = None
   )
   mBlock = bk.MiningBlock(mEnv)
   #print(mBlock)
   myLewysG.getBag().add(il.pickaxe)
   mBlock.explore(p, 1)
   '''
   
   # floor test
   #from floors import Floor
   #f1 = Floor(5, 1, [eBlock, sBlock, bBlock], [2, 1, 1], bk.StairsBlock())
   #print(f1)
   forestBoB = bk.BossBlock(
      bk.Environment(
         look = [
         "you arrive to the stairs that lead to the next floor. but "
         "you can't take them because something is nesting on it. "
         "in the middle of the web barring your path, you see a pupa."
         "not so happy to be troubled, it attacks you...",
         "the pupa breaks but you can't rejoice because something fell "
         "from it. you watch as it stretches its wings and screams at "
         "you. the butterfly hatched sooner than expected and its not "
         "too content of that..."
         ],
         res = None,
         hostile = [bl.s_Butterfreak, ml.s_Caterkiller],
         amenity = None
      )
   )
   info = forestBoB.explore(p, 3)
   if info[1] != None:
      print(info[1])
   '''f1Blocks = f1.build()
   current = 0
   while current < len(f1Blocks) and p.stillStands():
      print("\nB{}f: {}\n".format(current + 1, f1Blocks[current].name))
      sleep(1)
      f1Blocks[current].explore(p, f1.getHazardLevel())
      if p.stillStands():
         current += 1
         if current < len(f1Blocks):
            print("\nYou continue your exploration.\n")
         else:
            print("exhausted, you head back to the city.\n")
   # end of exploration loop
   myLewysG.getSkillSet().resetAll() # reset all skills cooldowns
   print(myLewysG.__str__(False))
   print(myLewysG.getBag())
   '''
   
   