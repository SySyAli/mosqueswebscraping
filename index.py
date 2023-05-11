import requests as req
from bs4 import BeautifulSoup

# This is a python script that scraps the Salatomatic website for all the Masjids in the USA
SALATOMATIC_URL = "https://www.salatomatic.com"
# This function scraps the main page of Salatomatic USA and gets the div that contains all the main state page
def getAllMasjidsinUSA():
    URL = SALATOMATIC_URL + "/reg/United-States/sPpaNwWSpq"
    r = req.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    sortedTableArray = []
    #print(soup.prettify())
    tableArray = soup.find_all('table')
    for table in tableArray:
        if(table.get_text().find("Alabama") != -1 and table.get_text().find("32") != -1):
            #print(table.prettify())
            #print("FOUND")
            sortedTableArray.append(table)
    importantTable = sortedTableArray[(len(sortedTableArray))-1]
    getStateMasjidLinks(importantTable)
    
# This function sorts through the table from the getAllMasjidsinUSA() function and gets the links to each state
def getStateMasjidLinks(importantTable):
    # this table contains the links each State Page (which contains the metroplitan areas)
    # Should be stored as [Name of the State, Link to the State]
    stateLinks = []
    for link in importantTable.find_all('a'):
        #print(link.get('href'))
        #print(link.string)
        link_url = SALATOMATIC_URL + "/reg/" + link.get('href')
        stateLinks.append([link.string, link_url])
        getMetropolitanMasjidLinks(link.string, link_url)
    #print(stateLinks)

# This function sorts through each link from the getStateMasjidLinks() function and gets the links to each metropolitan area
def getMetropolitanMasjidLinks(stateName, stateLink):
   #print(stateName)
    URL = stateLink
    r = req.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    # Format [metro name, link to metro]
    metropolitanAreaLinks = []
    for link in soup.find_all('a'):
        if(link.get('href').find("/sub/") != -1):
            #print(link.get('href'))
            #print(link.string)
            metropolitanAreaLinks.append([link.string, "https://www.salatomatic.com" + link.get('href')])
            getMasjidNamesAndLocations(link.string, "https://www.salatomatic.com" + link.get('href'))
    #print(metropolitanAreaLinks)
    #print(len(metropolitanAreaLinks))

# This function sorts through each link from the getMetropolitanMasjidLinks() function and gets the name and location of each masjid
def getMasjidNamesAndLocations(metropolitanAreaName, metropolitanAreaLink):
    print(metropolitanAreaName)
    URL = metropolitanAreaLink
    r = req.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    # Format [masjid name, location]
    masjidNamesAndLocations = []
    for div in soup.find_all('div', {'id': 'header', 'onclick': lambda value: value and 'location.href' in value}):
        print(div)
    #print(soup.prettify())

getAllMasjidsinUSA()