'''
# containers.py
# Items objects need to be carried and thus this module
# provide the Inventory class that can be used to represent
# a bag, a stall or a rack etc... also provides the definition
# for the Equipment which is a collection of 3 items that 
# impact the stats of a Playable. Finally, defines the Wallet
# which is more of currency manager.
# date: 6/27/21
# author: dnglokpor
'''

# imports
from base import STATS
from collectibles import genHash, Item, Gear

# Inventory object
class Inventory:
   '''this definition of the Inventory relies on an
   extensible dict model. a dict allows items to be quick
   to retrieve and sort. the contents are organized as 
   a dict of lists thus stackability is possible.
   also the Inventory keeps track of its size as well 
   because it is limited and its size is defined at 
   construction.'''
   
   def __init__(self, size = 30):
      '''construct an empty dict at this point and
      set the size.'''
      self.contents = dict()
      self.size = size
   
   # getters
   def isEmpty(self):
      '''return True if there are no items in the Inventory.'''
      return len(self.contents.items()) == 0
   def hasSpace(self):
      '''return True if there is enough space to add a new
      item to the contents.'''
      return len(self.contents.items()) < self.size
   def getStackOf(self, k: int) -> list:
      '''return the stack of items by at this key.'''
      if self.contents.__contains__(k):
         return self.contents.get(k)
   def takeOut(self, iName: str, qty = 1) -> list:
      '''takes out of the bag an item identified by
      its name in the quantity requested if available.
      return a list of the items taken out. the 
      quantity must be absolutely positive (> 0).'''
      if qty <= 0:
         raise ValueError("quantity must be absolutely\
positive (> 0).")
      found = list() # empty list
      k = genHash(iName)
      if self.contains(iName): # we have some
         stack = self.getStackOf(k)
         if len(stack) >= qty: # enough
            for i in range(qty): # take out then
               found.append(stack.pop())
         if len(stack) == 0: # out of stock
            # clear slot from bag
            v = self.getStackOf(k)
            self.contents = self.shrink((k, v))
      
      return found
            
   # setters
   def add(self, itm: Item) -> bool:
      '''add a new item to the bag, based on its ID. if the 
      item was not yet in bag, it adds it; else it stacks
      it. this method calls helper methods to "extend" the
      size of the dict. also the size of the bag cannot
      go over the defined size thus no "new item" can be
      added once the max size is reached but stackability
      is still possible.
      '''
      k = itm.getID()
      done = False
      if self.isEmpty():
         # just add that one item.
         self.contents = dict({k: [itm,]})
         done = True
      else:
         if self.contents.__contains__(k):
            # item already exists in bag so stack
            stack = self.contents.get(k)
            stack.append(itm)
            self.contents.__setitem__(k, stack)
            done = True
         else: # item doesn't exist in bag yet
            if self.hasSpace():
               self.contents = self.expand(itm)
               done = True

      return done
   def addMulti(self, itm: Item, qt= 1):
      '''add multiple copies of the same item to
      the bag.'''
      done = False
      i = 0
      while self.hasSpace() and not done:
         if self.add(itm.copy()): # different copies
            i += 1
            done = i == qt
      return done
      
   # iterator that goes through each item of the bag one
   # stack at the time
   def __iter__(self):
      '''initializes the iterable functionality of the
      Inventory object.'''
      self.stackIdx = 0
      self.contentsList = list(self.contents.values()) 
      return self
   
   def __next__(self):
      '''returns the next stack of items in the inventory until
      all stacks have been traversed.'''
      # save old value of the stack index
      sIdx = self.stackIdx
      
      # stop check
      if sIdx >= len(self.contentsList):
         raise StopIteration # cleared all stacks
      
      # get contents
      stack = self.contentsList[sIdx]
      
      # increment
      self.stackIdx += 1 # next stack
      
      # return current item
      return stack
   
   # helpers
   def expand(self, newEntry: Item) -> dict:
      '''to expand the bag, we are basically creating a
      new dict to replace the old one. this means extracting
      the contents of the previous to build the new one.'''
      newContents = list(self.contents.items())
      newContents.append((newEntry.getID(), [newEntry,]))
      return dict(newContents)
   def shrink(self, outOfStock: tuple) -> dict:
      '''same procedure as self.expand() but this time
      returns a new dict without the "outOfStock"
      item.'''
      newContents = newContents = list(self.contents.items())
      newContents.remove(outOfStock)
      return dict(newContents)
   def contains(self, iName: str) -> bool:
      '''checks if an item of this name is in the bag.
      return "True" if it does, False elsewise.'''
      h = genHash(iName)
      return self.contents.__contains__(h)
   
   # override tostring
   def __str__(self) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = "Bag contents:\n"
      if self.isEmpty():
         description += "nothing to see here..."
      else:
         # items and quantity
         for idx, stack in enumerate(self.contents.values()):
            # first item in stack represent stack
            description += "{:15s} x{:3d} ".format(
               stack[0].getName(), len(stack))
            if idx != len(self.contents.keys()) - 1:
               description += '\n'
      return description

# all Equipment slots:
SLOTS = ["WPN", "ARM", "ACC"]

# Equipment object
class Equipment(dict):
   '''the collection of the 3 gear that a playable can
   have at the time. based off a dict for convenience.'''
   
   def __init__(self):
      '''construction requires no actual gear. defines
      placeholders for them.'''
      super().__init__({"WPN": None, "ARM": None, "ACC": None})
  
   # getters
   def getGear(self, slot: str):
      '''return the requested gear out of the Equipment.
      if nothing was equiped there, return "None".'''
      g = None
      if(self.__contains__(slot)):
         g = self.get(slot)
      return g
   
   def getEqtBonus(self) -> list:
      '''returns as a list formated in the order of the 
      base.STATS the combined stats bonuses (or maluses)
      conferred by the equipment pieces.'''
      comb = [0, 0, 0, 0, 0, 0, 0]
      for g in self.values():
         if g != None: # not empty slot
            for sName, val in g.getStats():
               comb[STATS.index(sName)] += val
      return comb
   
   # setters
   def setGear(self, gear: Gear) -> Gear:
      '''assign passed gear to the right slot. this depends
      on the existence of the "t" attribute of passed
      gear thus if gear doesn't have it, ValueError is
      raised. returns the old gear set at the slot if any
      or just None.'''
      old = None
      slot = None
      try:
         slot = gear.t
      except AttributeError: # gear without a "t" attribute
         raise ValueError("passed gear is not a Weapon, Armor\
or Accessory type object.")
      old = self.get(slot)
      self.__setitem__(slot, gear)
      return old         
   
   # override tostring
   def __str__(self, short = True) -> str:
      '''return a string representing this object for
      printing purposes.'''
      description = str()
      for t, gear in self.items():
         description += "[{}] -> ".format(t)
         if gear is not None:
            description += "<{}>\n".format(gear.getName())
         else:
            description += "not set\n"
      return description

# Wallet object
class Wallet:
   '''Class that represents the money pouch.'''
   def __init__(self, initial_balance = 0):
      self.contents = initial_balance # default value
   
   # getters
   def getBalance(self):
      return self.contents
   
   # setters
   def pocket(self, amount):
      '''Adds the amount to your wallet. amount will
      be treated as an absolute value.'''
      self.contents += abs(amount)
   
   def pay(self, amount):
      '''Takes out the amount to your wallet. Return
      the amount requested if possible. else it return
      "None".'''
      out = None
      amount = abs(amount)
      if self.contents >= amount: # you can afford it
         self.contents -= amount
         out = amount
      return out
   
   # override tostring
   def __str__(self):
      '''return a string representing this object for
      printing purposes.'''
      if self.contents != 1:
         return "{} coins".format(self.contents)
      else:
         return "1 coin"

# test platform
if __name__ == "__main__":
   arrow = Item(
      "Arrow",
      "40cm of wood crowned by a sharpened steel head and"
      " feathers in the back. rangers' favorite.", 
      3
   )
   pelt = Item(
      "Pelt",
      "freshly skinned pelt of a small dungeon denizen.",
      10
   )
   smallFeathers = Item(
      "Small Feathers",
      "a few small but sturdy feathers that float in the wind.",
      5
   )
   myBag = Inventory()
   myBag.addMulti(arrow, 30)
   myBag.addMulti(pelt, 10)
   myBag.addMulti(smallFeathers, 7)
   # print(myBag)
   for item in myBag:
      print("{} {}".format(len(item), item[0].getName()))