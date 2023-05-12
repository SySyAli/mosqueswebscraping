# Salatomatic Masjid Web Scraper

This Python script is designed to scrape the Salatomatic website to obtain information about all the Masjids (mosques) in the United States. It utilizes the `requests` and `BeautifulSoup` libraries to extract data directly from the website.

### Prerequisites

Before running the script, make sure you have the following libraries installed:

- `requests`: Used for making HTTP requests to fetch web pages.
- `BeautifulSoup`: Used for parsing and navigating HTML content.

You can install these libraries using pip:

```
pip install requests beautifulsoup4
```

### Script Overview

1. The script starts by defining several helper functions to scrape the Salatomatic website.

2. The `getAllMasjidsinUSA()` function fetches the main page of Salatomatic USA and retrieves the `<div>` element that contains all the state information. It returns a list of all the Masjids in the USA, in alphabetical order of state.

3. The `getStateMasjidLinks()` function parses the table from the previous step and extracts the links to each state's page. It returns a list of Masjids in each state, sorted by metropolitan areas.

4. The `getMetropolitanMasjidLinks()` function follows each state's link and extracts the links to each metropolitan area's page. It returns a list of Masjids in each metropolitan area.

5. The `getMasjidNamesAndLocations()` function follows each metropolitan area's link and extracts the name and location of each Masjid. It returns a list of dictionaries for a metropolitan area containing the state name, metropolitan area name, Masjid name, and Masjid location.

6. The `getMasjidPhoneNumber()` function follows each Masjid's link and retrieves the phone number if it exists. It returns a dictionary containing the state name, metropolitan area name, Masjid name, Masjid location, and phone number.

7. The `save_to_csv()` function saves the obtained Masjid information to a CSV file. It accepts the data (a list of dictionaries) and the filename as parameters.

8. Finally, the script calls the necessary functions to scrape the Salatomatic website and saves the obtained Masjid information to a CSV file named "masjid_data.csv".

### Usage

To use the script, ensure you have installed the required libraries and then simply run the script. It will scrape the Salatomatic website for all the Masjids in the United States and save the information to a CSV file named "masjid_data.csv" in the same directory.

Please note that web scraping should be done responsibly and in accordance with the website's terms of service. Ensure that you are not overwhelming the website with requests and consider adding appropriate delays between requests to avoid any issues.

Feel free to modify the script as needed to suit your specific requirements and data structure. Enjoy!
