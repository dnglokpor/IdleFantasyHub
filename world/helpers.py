'''
# helpers.py
# contains module-wide methods that provide quick computation
# needs.
# date: 9/23/21
# author: dnglokpor
'''

# imports
from random import choice

def rndGen(max = 10):
   '''randomly allocates a number between 1 and max for
   the luck stat.'''
   return choice(range(max)) + 1