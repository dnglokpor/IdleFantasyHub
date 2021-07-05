'''
# elements.py
# IdleFantasyHub's world has elements which are special
# properties of things that allows them to have affinity
# or not with other things of the world. not everything
# has an element. there are 4 elements total: aeola > gaia
# > aqua > vulcan. there is also an element that represent
# the absence of element: noelm
# date: 7/4/21
# author: dnglokpor
'''

class Element:
   '''the base element object on which the actual elements.
   defines the name and value attributes and override the
   greater than and less than operators based on their
   value.'''
   
   def __init__(self, name: str, value: int):
      self.name = name
      self.value = value
   
   # getter
   def getName(self):
      return self.name
   
   # no setters for elements
   
   # others
   def __gt__(self, other):
      '''each element is effective on the element that
   has one more value than it. if the value is 0, then
   it doesn't matter.'''
      if self.value == 0 or other.value == 0:
         return False
      else:
         weaker = 0
         if self.value == 4:
            weaker = 1 # round around
         else:
            weaker = self.value + 1
         return other.value == weaker
   def __lt__(self, other):
      '''each element is weak to the element that has one
      less value than it. if the value is 0, then it doesn't
      matter.'''
      if self.value == 0 or other.value == 0:
         return False
      else:
         stronger = 0
         if self.value == 1:
            stronger = 4 # round around
         else:
            stronger = self.value - 1
         return other.value == stronger
   def __eq__(self, other):
      '''two elements are equal if they have equal value
      attributes.'''
      return self.value == other.value
   
   # override tostring
   def __str__(self):
      return self.name

# predefined elements
NOELM = Element("Noelm", 0)
AEOLA = Element("Aeola", 1)
GAIA = Element("Gaia", 2)
AQUA = Element("Aqua", 3)
VULCAN = Element("Vulcan", 4)

if __name__ == "__main__":
   print(AEOLA <= AEOLA)