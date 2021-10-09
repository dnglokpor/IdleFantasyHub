'''
# helpers.py
# contains module-wide methods that provide quick computation
# needs.
# date: 9/23/21
# author: dnglokpor
'''

# imports
from random import choice
import sys
import time as tm

# random gen 1 - maxValue
def rndGen(max = 10):
   '''randomly allocates a number between 1 and max for
   the luck stat.'''
   return choice(range(max)) + 1
# print to file instead of stdout
def fprint(msg: str, stream = sys.stdout):
   '''prints to the specified file.'''
   if type(msg) != type(str()):
      msg = msg.__str__()
   if stream != sys.stdout:
      stream = open(stream, "a+")
   print(msg, file = stream)
# convert epoch to a time string
def timeString(seconds: int) -> str:
   '''return a "XXhXXminXXs" format time string from the seconds.'''
   sec = seconds % 60
   min = seconds // 60
   hour = min // 60
   if hour != 0:
      min = min % 60   
   tString = "{}h{}min{}s".format(hour, min, sec)
   return tString