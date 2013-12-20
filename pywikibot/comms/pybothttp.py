# -*- coding: utf-8  -*-
"""
Basic HTTP access interface.

This module handles communication between the bot and the HTTP threads.

This module is responsible for
    - Setting up a connection pool
    - Providing a (blocking) interface for HTTP requests
    - Translate site objects with query strings into urls
    - Urlencoding all data
    - Basic HTTP error handling
"""

#
# (C) Pywikipedia bot team, 2007
#
# Distributed under the terms of the MIT license.
#

__version__ = '$Id$'
__docformat__ = 'epytext'
#from http.cookiejar import LWPCookieJar
from http.cookiejar import LoadError
import queue
#import urllib
#import urllib.parse
#import logging
import atexit
from pywikibot.bot import log, debug

from ssl import SSLError as SSLHandshakeError
#from pywikibot import config
from pywikibot.exceptions import FatalServerError, Server504Error
import pywikibot
import pywikibot.bot
from urllib.request import urljoin
from . import threadedhttp
import pywikibot.version

class HTTP :
    def __init__(self, config):
        self._logger = "comm.http"
        # global variables

        # The OpenSSL error code for
        #   certificate verify failed
        # cf. `openssl errstr 14090086`
        self.SSL_CERT_VERIFY_FAILED = ":14090086:"

        # the User-agent: header. The default is
        # '<script>/<revision> Pywikipediabot/2.0', where '<script>' is the currently
        # executing script and version is the SVN revision of Pywikipediabot.
        self.USER_AGENT_FORMAT = '{script}/r{version[rev]} Pywikipediabot/2.0'
        self.useragent = self.USER_AGENT_FORMAT.format(script=pywikibot.bot.calledModuleName(),
                                         version=pywikibot.version.getversiondict())
        self.numthreads = 1
        self.threads = []

        self.connection_pool = threadedhttp.ConnectionPool()
        self.http_queue = queue.Queue()

        self.cookie_jar = threadedhttp.LockableCookieJar(config.datafilepath("pywikibot.lwp"))
        try:
            self.cookie_jar.load()
        except (IOError, LoadError):
            debug("Loading cookies failed.", self._logger)
        else:
            debug("Loaded cookies from file.", self._logger)


        # Build up HttpProcessors
        log('Starting %di threads...' % self.numthreads)
        for i in range(self.numthreads):
            proc = threadedhttp.HttpProcessor(
                self.http_queue, 
                self.cookie_jar, 
                self.connection_pool)
            proc.setDaemon(True)
            self.threads.append(proc)
            proc.start()

        atexit.register(self._flush)
        #self.pywikibot.cookie_jar = cookie_jar

    # Prepare flush on quit
    def _flush(self):
        for i in self.threads:
            self.http_queue.put(None)
        log('Waiting for threads to finish... ')
        for i in self.threads:
            i.join()
        log("All threads finished.")


    # export cookie_jar to global namespace



    def request(self,site, uri, ssl=False, *args, **kwargs):
        """Queue a request to be submitted to Site.

        All parameters not listed below are the same as
        L{httplib2.Http.request}, but the uri is relative

        If the site argument is None the uri has to be absolute and is
        taken. In this case ssl is ignored. Used for requests to non wiki
        pages.

        @param site: The Site to connect to
        @param uri: the URI to retrieve (relative to the site's scriptpath)
        @param ssl: Use https connection
        @return: The received data (a unicode string).

        """
        if site:
            if ssl:
                print ("use ssl")
                proto = "https"
                host = site.ssl_hostname()
                uri = site.ssl_pathprefix() + uri
            else:
                print ("dont use ssl")
                proto = site.protocol()
                host = site.hostname()

            print ("proto:%s" % proto)
            print ("host:%s" % host)
            baseuri = urljoin("%(proto)s://%(host)s" % locals(), uri)
        else:
            baseuri = uri

        # set default user-agent string
        kwargs.setdefault("headers", {})
        kwargs["headers"].setdefault("user-agent", self.useragent)
        request = threadedhttp.HttpRequest(baseuri, *args, **kwargs)
        print (self.http_queue)
        self.http_queue.put(request)
        print (self.http_queue)
        print ("before lock")
        request.lock.acquire()
        print ("after lock")

        #TODO: do some error correcting stuff
        #print("debug:%s" % request.data)
        if isinstance(request.data, SSLHandshakeError):
            if self.SSL_CERT_VERIFY_FAILED in str(request.data):
                raise FatalServerError(str(request.data))

        #if all else fails
        if isinstance(request.data, Exception):
            raise Exception(request.data)
            
        if request.data is not None :
            #print("debug:%s" % request.data)
            #print("debug:%s" % request.data[0])
            if request.data[0].status == 504:
                raise Server504Error("Server %s timed out" % site.hostname())
            if request.data[0].status != 200:
                pywikibot.warning("Http response status %(status)s"
                                % {'status': request.data[0].status})

            return request.data[1]
        else:
            raise Exception("no data")

# global object


def global_http():
    from pywikibot.config import loadconfig
    return HTTP(config = loadconfig())


def request(site, uri, ssl=False, *args, **kwargs):
    return global_http.request(site, uri, ssl=False, *args, **kwargs)
