'''
# containers.py
# Items objects need to be carried and thus this module
# provide the Inventory class that can be used to represent
# a bag, a stall or a rack etc... also provides the definition
# for a Wallet which is more of currency manager.
# date: 6/27/21
# author: dnglokpor
'''

# imports
from collectibles import Item, genHash

# test import
from itemLib import arrow, pelt, smallFeathers

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
   
   # iterator that goes through each item of the bag one
   # at the time
   def __iter__(self):
      '''initializes the iterable functionality of the
      Inventory object.'''
      self.stackIdx = 0
      self.itemIdx = 0
      self.contentsList = list(self.contents.values()) 
      return self
   
   def __next__(self):
      '''returns the next item in the inventory until
      all items have been recovered.'''
      # save old value of the stack index
      sIdx = self.stackIdx
      
      # stop check
      if sIdx >= len(self.contentsList):
         raise StopIteration # cleared all stacks
      
      # get contents
      iIdx = self.itemIdx
      stack = self.contentsList[sIdx]
      
      # increment
      if self.itemIdx < len(stack) - 1:
         self.itemIdx += 1 # next item
      else:
         self.stackIdx += 1 # next stack
         self.itemIdx = 0 # first item
      
      # return current item
      return stack[iIdx]
   
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
   myBag = Inventory()
   for i in range(10):
      myBag.add(arrow)
   for i in range(2):
      myBag.add(pelt)
   for i in range(7):
      myBag.add(smallFeathers)
   print(myBag)
   for item in myBag:
      print(item)
   