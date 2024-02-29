# Changes:

* Split capabilities into relevant classes.
* Added a capability for the user to specify a specific league they're interested in - including using abbreviations e.g Prem for Premier League, and fuzzy matching to account for typos.
* Clean data stage now includes a filter which removes the data for leagues the user isn't interested in.
* Added some date helpers for what I expect are common options - today, yesterday, tomorrow or custom.

# Required Python Packages

* pip install requests
* pip install BeautifulSoup
* pip install fuzzywuzzy
* pip install python-Levenshtein (option speedup package)

# Plans & Aims:

* Extension to scrape league-table data.
* Consider a database or similar to store scraped data, the 'filters' used and the associated cleaned data.
* Use This Scraping Data To Find Other More Interesting Data, e.g match stats, line-ups, MOTM or commentary transcripts.
* Extend ^ scraping to get similar data from other websites e.g sky sports.
* Consider storage and utilisation of that data.


# Football Web Scraping With BeautifulSoup - Original
Here I use BeautifulSoup to scrape data of football fixtures from the BBC sport website, from the specified date which is inputted by the user. Returning the result in a neat format in python. Web Scraping carried out using pythons libraries BeautifulSoup and Requests.

The user is asked to input a date in the format (YYYY-MM-DD), as this is what is on the end of the URL for the fixtures for that day from the BBC Sport Website.

```Enter the date that you would like to see fixtures from in the format (YYYY-MM-DD): 2022-01-27```

This will then display the fixtures for that chosen date:

<img width="300" alt="results1" src="https://user-images.githubusercontent.com/53832520/151462403-6f8307ad-b7cc-42de-9212-04a48642265c.png">

Requesting for a date in the future:

```Enter the date that you would like to see fixtures from in the format (YYYY-MM-DD): 2022-02-02```

<img width="400" alt="results2" src="https://user-images.githubusercontent.com/53832520/151462760-d7cdec04-c881-48fa-9b07-0051409368ee.png">
