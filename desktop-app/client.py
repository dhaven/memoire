import requests

url = "http://127.0.0.1:8000/polls/"
image = {'file':open('sphere_green.png','rb')}

s = requests.session()
r = s.get(url)

headers = {'X-CSRFToken': s.cookies["csrftoken"]}
r = s.post(url, files = image, cookies = s.cookies,headers=headers)