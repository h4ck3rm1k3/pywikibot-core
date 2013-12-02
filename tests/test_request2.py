import urllib.request
f = urllib.request.urlopen("https://en.wikipedia.org/w/api.php")
print(f.read())
