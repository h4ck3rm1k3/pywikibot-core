import datetime
import difflib
#import logging
import math
import re
#import sys
import threading
from queue import Queue
import datetime
from config import loadconfig
import threading
from queue import Queue

from pywikibot.bot import warning, output, inputChoice, debug, log
import pywikibot.comms.pybothttp

import atexit

# Create a separate thread for asynchronous page saves (and other requests)

class ThreadServer :
    def __init__(self):
        self.config = loadconfig()
        # queue to hold pending requests
        self.page_put_queue = Queue(self.config.max_queue_size)
        # set up the background thread
        _putthread = threading.Thread(target=self.async_manager)
        # identification for debugging purposes
        _putthread.setName('Put-Thread')
        _putthread.setDaemon(True)
        
        self.stopped = False
        atexit.register(self.stopme)

    def remaining(self):
        
        remainingPages = self.page_put_queue.qsize() - 1
        # -1 because we added a None element to stop the queue
        remainingSeconds = datetime.timedelta(
            seconds=(remainingPages * self.config.put_throttle))
        return (remainingPages, remainingSeconds)

    def stopme(self):
        """Drop this process from the throttle log, after pending threads finish.

        Can be called manually if desired, but if not, will be called automatically
        at Python exit.
        """

#        global stopped
        _logger = "wiki"

        if not self.stopped:
            debug("stopme() called", _logger)


            self.page_put_queue.put((None, [], {}))
            stopped = True

            if self.page_put_queue.qsize() > 1:
                output('Waiting for %i pages to be put. Estimated time remaining: %s'
                       % self.remaining())

            while(self._putthread.isAlive()):
                try:
                    self._putthread.join(1)
                except KeyboardInterrupt:
                    answer = inputChoice("""\
    There are %i pages remaining in the queue. Estimated time remaining: %s
    Really exit?""" % self.remaining(),
                        ['yes', 'no'], ['y', 'N'], 'N')
                    if answer == 'y':
                        return

        # only need one drop() call because all throttles use the same global pid
        try:
            #TODO : list(pywikibot._sites.values())[0].throttle.drop()
            log("Dropped throttle(s).")
        except IndexError:
            pass

    def async_manager(self):
        """Daemon; take requests from the queue and execute them in background."""
        while True:
            (request2, args, kwargs) = page_put_queue.get()
            if request2 is None:
                break
            pywikibot.comms.pybothttp.request(*args, **kwargs)

    def async_request(self,request, *args, **kwargs):
        """Put a request on the queue, and start the daemon if necessary."""
        if not _putthread.isAlive():
            try:
                page_put_queue.mutex.acquire()
                try:
                    _putthread.start()
                except (AssertionError, RuntimeError):
                    pass
            finally:
                page_put_queue.mutex.release()
        page_put_queue.put((pywikibot.comms.pybothttp.request, args, kwargs))

