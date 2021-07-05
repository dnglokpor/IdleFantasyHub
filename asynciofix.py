'''
# asynciofix.py
# adds code recovered from https://stackoverflow.com/questions/52232177/runtimeerror-timeout-context-manager-should-be-used-inside-a-task
# written by Abraham Murciano Benzadon for replacing
# buggy asyncio.run() method.
# author: Abraham Murciano Benzadon
'''

import asyncio
import nest_asyncio

def asyncio_run(future, as_task=True):
   """
   A better implementation of `asyncio.run`.

   :param future: A future or task or call of an async method.
   :param as_task: Forces the future to be scheduled as task (needed for e.g. aiohttp).
   """

   try:
      loop = asyncio.get_running_loop()
   except RuntimeError:  # no event loop running:
      loop = asyncio.new_event_loop()
      return loop.run_until_complete(_to_task(future, as_task, loop))
   else:
      nest_asyncio.apply(loop)
      return asyncio.run(_to_task(future, as_task, loop))


def _to_task(future, as_task, loop):
   if not as_task or isinstance(future, asyncio.Task):
      return future
   return loop.create_task(future)