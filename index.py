import requests as req

URL = "https://hirr.hartsem.edu/mosque/database.html"

r = req.get(URL)

print(r.text)