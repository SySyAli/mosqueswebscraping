import requests as req
from bs4 import BeautifulSoup


# Scraping first website to generate CSV 
URL = "https://hirr.hartsem.edu/mosque/database.html"

r = req.get(URL)

soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

# Format is for each entry is: [stateLink, stateName]
stateLinks = []

for link in soup.find_all('option')[1:]:
    
    stateName = " ".join(link.string.split())
    stateLinks.append([link.get('value'),stateName])
    #print(link.get('value'))
print(stateLinks)

# Go through each link and get the data
for link in stateLinks:
    r = req.get(link[0])
    soup = BeautifulSoup(r.content, 'html5lib')
    for table in soup.find_all(bgcolor = "#E2E2E2"):
        print(table)
    
    #print(soup.prettify())
