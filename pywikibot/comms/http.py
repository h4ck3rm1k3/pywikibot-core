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

import queue
#import urllib
import urllib.parse
#import logging
import atexit

try:
    from httplib2 import SSLHandshakeError
except ImportError:
    from ssl import SSLError as SSLHandshakeError
from pywikibot import config
from pywikibot.exceptions import FatalServerError, Server504Error
import pywikibot
import http.cookiejar
from . import threadedhttp
import pywikibot.version

_logger = "comm.http"


# global variables

# The OpenSSL error code for
#   certificate verify failed
# cf. `openssl errstr 14090086`
SSL_CERT_VERIFY_FAILED = ":14090086:"

# the User-agent: header. The default is
# '<script>/<revision> Pywikipediabot/2.0', where '<script>' is the currently
# executing script and version is the SVN revision of Pywikipediabot.
USER_AGENT_FORMAT = '{script}/r{version[rev]} Pywikipediabot/2.0'
useragent = USER_AGENT_FORMAT.format(script=pywikibot.calledModuleName(),
                                     version=pywikibot.version.getversiondict())
numthreads = 1
threads = []

connection_pool = threadedhttp.ConnectionPool()
http_queue = queue.Queue()

cookie_jar = threadedhttp.LockableCookieJar(config.datafilepath("pywikibot.lwp"))
try:
    cookie_jar.load()
except (IOError, http.cookiejar.LoadError):
    pywikibot.debug("Loading cookies failed.", _logger)
else:
    pywikibot.debug("Loaded cookies from file.", _logger)


# Build up HttpProcessors
pywikibot.log('Starting %(numthreads)i threads...' % locals())
for i in range(numthreads):
    proc = threadedhttp.HttpProcessor(http_queue, cookie_jar, connection_pool)
    proc.setDaemon(True)
    threads.append(proc)
    proc.start()


# Prepare flush on quit
def _flush():
    for i in threads:
        http_queue.put(None)
    pywikibot.log('Waiting for threads to finish... ')
    for i in threads:
        i.join()
    pywikibot.log("All threads finished.")
atexit.register(_flush)

# export cookie_jar to global namespace
pywikibot.cookie_jar = cookie_jar


def request(site, uri, ssl=False, *args, **kwargs):
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
            proto = "https"
            host = site.ssl_hostname()
            uri = site.ssl_pathprefix() + uri
        else:
            proto = site.protocol()
            host = site.hostname()
        baseuri = urllib.parse.urljoin("%(proto)s://%(host)s" % locals(), uri)
    else:
        baseuri = uri

    # set default user-agent string
    kwargs.setdefault("headers", {})
    kwargs["headers"].setdefault("user-agent", useragent)
    request = threadedhttp.HttpRequest(baseuri, *args, **kwargs)
    http_queue.put(request)
    request.lock.acquire()

    #TODO: do some error correcting stuff
    if isinstance(request.data, SSLHandshakeError):
        if SSL_CERT_VERIFY_FAILED in str(request.data):
            raise FatalServerError(str(request.data))

    #if all else fails
    if isinstance(request.data, Exception):
        raise request.data

    if request.data[0].status == 504:
        raise Server504Error("Server %s timed out" % site.hostname())

    if request.data[0].status != 200:
        pywikibot.warning("Http response status %(status)s"
                          % {'status': request.data[0].status})

    return request.data[1]
