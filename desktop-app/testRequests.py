import requests

r = requests.put('http://httpbin.org/put', data = {'key':'value'})
print r.text