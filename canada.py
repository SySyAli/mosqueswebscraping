import requests as req
from bs4 import BeautifulSoup
import re
import csv
# This is a python script that scraps the Salatomatic website for all the Masjids in the USA

# This function scraps the main page of Salatomatic USA and gets the div that contains all the main state page
# Returns a list of all the masjids in the USA by state
# Format: [state#0, state#1, ...]
def getAllMasjidsinCanada():
    print("Canada")
    allMasjidInformation = []
    URL = "https://www.salatomatic.com/reg/Canada/paKMeao7gi"
    r = req.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    sortedTableArray = []
    #print(soup.prettify())
    tableArray = soup.find_all('table', width= "800", cellpadding="0", cellspacing="0")
    for table in tableArray:
        if(table.get_text().find("Alberta") != -1 and table.get_text().find("52") != -1):
            #print(table.prettify())
            print("FOUND")
            sortedTableArray.append(table)
            break
    importantTable = sortedTableArray[(len(sortedTableArray))-1]
    #print(importantTable)
    return getStateMasjidLinks(importantTable)
    
# This function sorts through the table from the getAllMasjidsinUSA() function and gets the links to each state
# Returns a list of all the masjids in a state, sorted by metro area
# Format: [state#0, state#1, ...]
def getStateMasjidLinks(importantTable):
    # this table contains the links each State Page (which contains the metroplitan areas)
    # Should be stored as [Name of the State, Link to the State]
    stateLinks = []
    for link in importantTable.find_all('a'):
        #print(link.get('href'))
        #print(link.string)
        link_url = "https://www.salatomatic.com/reg/" + link.get('href')
        stateLinks.extend(getMetropolitanMasjidLinks(link.string, link_url))
    #print(stateLinks)
    return stateLinks    
    
# This function sorts through each link from the getStateMasjidLinks() function and gets the links to each metropolitan area
# Returns a list of all the masjids in a metropolitan areas of the state
# [metropolitanArea#0, metropolitanArea#1, ...]
def getMetropolitanMasjidLinks(stateName, stateLink):
    print(stateName)
    URL = stateLink
    r = req.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    # Format [metro name, link to metro]
    metropolitanAreaLinks = []
    for link in soup.find_all('a'):
        if(link.get('href').find("/sub/") != -1):
            #print(link.get('href'))
            #print(link.string)
            metropolitanAreaLinks.extend(getMasjidNamesAndLocations(stateName, link.string, "https://www.salatomatic.com" + link.get('href')))
    print(metropolitanAreaLinks)
    return metropolitanAreaLinks 
    #print(metropolitanAreaLinks)
    #print(len(metropolitanAreaLinks))

# This function sorts through each link from the getMetropolitanMasjidLinks() function and gets the name and location of each masjid
# Returns a list of all the masjids in the metropolitan area
# Return: [masjid_info#0, masjid_info#1, ...]
def getMasjidNamesAndLocations(stateName, metropolitanAreaName, metropolitanAreaLink):
    print(metropolitanAreaName)
    URL = metropolitanAreaLink
    r = req.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    # Format [salatomatic link, masjid name, location]
    metroInfo = []
    for div in soup.find_all('div', {'id': 'header', 'onclick': lambda value: value and 'location.href' in value}):
        masjidName = div.find('div', class_= 'titleBS').a.string
        masjidLink = "https://www.salatomatic.com" +  div.find('div', class_= 'titleBS').a['href']
        masjidLocation = div.find('div', class_= 'tinyLink').string
        masjidInfo = getMasjidPhoneNumber(stateName, metropolitanAreaName, masjidName, masjidLocation, masjidLink)
        if(masjidInfo != None):
            metroInfo.append(masjidInfo)
    return metroInfo
    #print(masjidLinksNamesAndLocations)

# This masjid gets the phone number of each masjid. The phone number may be None.
# Returns: {State Name, Metro Area, Masjid Name, Masjid Location, Phone Number}
def getMasjidPhoneNumber(stateName, metropolitanAreaName, masjidName, masjidLocation, masjidLink):
    URL = masjidLink
    r = req.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    # Check text of page to see if phone number exists
    #print(soup.find_all('div', class_= 'midLink'))
    # format only sunni masjid
    phoneNumbers = re.findall(r"\(\d\d\d\)\s\d\d\d-\d\d\d\d", soup.get_text())
    if(len(phoneNumbers) == 0):
        phoneNumbers = None
    else:
        phoneNumbers = phoneNumbers[0]
    if(soup.get_text().find("SUNNI") != -1):
        masjid_data = {"State": stateName, "Metropolitan Area": metropolitanAreaName, "Masjid Name" : masjidName, "Masjid Location" : masjidLocation, "Phone Number" : phoneNumbers}
        print(masjid_data)
        return masjid_data
    else:
        return None



def save_to_csv(data, filename):
    csv_file = filename
    fieldnames = ["State", "Metropolitan Area", "Masjid Name", "Masjid Location", "Phone Number"]
    with open(csv_file, mode="w",encoding='utf-8', errors='ignore', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Write the header row
        writer.writeheader()
        # Write the data rows
        writer.writerows(data)
    print("CSV file created successfully.")

# TODO:  Format into an excel sheet
allMasjidInfo = getAllMasjidsinCanada()

save_to_csv(allMasjidInfo, "masjid_data.csv")
