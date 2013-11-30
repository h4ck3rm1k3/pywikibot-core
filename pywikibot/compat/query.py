import pywikibot
from pywikibot.data import api
from pywikibot import deprecated
from pywikibot import deprecate_arg


@deprecated("pywikibot.data.api.Request")
@deprecate_arg("useAPI", None)
@deprecate_arg("retryCount", None)
@deprecate_arg("encodeTitle", None)
def GetData(request, site=None, back_response=False):
    if site:
        request['site'] = site

    req = api.Request(**request)
    result = req.submit()

    if back_response:
        pywikibot.warning("back_response is no longer supported; an empty response object will be returned")
        import io
        res_dummy = io.StringIO()
        res_dummy.__dict__.update({'code': 0, 'msg': ''})
        return res_dummy, result
    return result
