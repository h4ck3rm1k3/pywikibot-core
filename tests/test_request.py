from http.client import HTTPSConnection
from base64 import b64encode

#https://
c = HTTPSConnection("en.wikipedia.org")

c.request('GET', '/w/api.php', headers={})
#get the response back
res = c.getresponse()
# at this point you could check the status etc
# this gets the page text
data = res.read()  
print(data)
