import requests

URL = "https://www.espn.com/"
page = requests.get(URL)

print(page.text)
