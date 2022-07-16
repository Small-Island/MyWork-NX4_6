import requests
res = requests.get('http://api.ipify.org/')
print(res.text)
