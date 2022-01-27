import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored
from leagues import Leagues


def date_function():
    date = input("Enter the date that you would like to see fixtures from in the format (YYYY-MM-DD): ")
    return date

def scraping(date):
    url = "https://www.bbc.co.uk/sport/football/scores-fixtures/" + date
    html_content = requests.get(url).text


    soup = BeautifulSoup(html_content, "html.parser")


    #the data I want is within these classes and these tags
    tags = ["span", "h3"]
    classes = (['gel-minion sp-c-match-list-heading',
                "gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc",
                "sp-c-fixture__status-wrapper qa-sp-fixture-status",
                'sp-c-fixture__number sp-c-fixture__number--time', #kick-off time
                "sp-c-fixture__number sp-c-fixture__number--home", #who is home team
                "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft",
                "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport",
                "sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--live-sport",
                "sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft"]) #league title


    

    scraper = soup.find_all(tags, attrs={'class': classes})

    data = [i.get_text() for i in scraper]
    if len(data) == 0:
        print("No fixtures today!")
    else:
        return data


def clean_data(data):

    #the data goes Home - Time - Away - ' '. As it expects a time but this is instead blank for games that hjavent kicked off yet.
    #so below i switch the blank with the time and delete he origianl time. Also this makes it easier when printing out the data.

    indicies = []
    for index, item in enumerate(data):
        if item == '':
            data[index] = data[index - 2]
            indicies.append(index - 2)


    for index in sorted(indicies, reverse=True):
        del data[index]

    data = ['TBC' if word == 'TBCTo be Confirmed' else word for word in data]
    

    return data



def print_data(data):

    i=0

    #these words are when i know to print a new line!
    stoppers = ["TBC","FT","HT","P","AET"]

    #only want to print a "vs" after the first team then stop it for the second, so use this to toggle.
    while i < len(data):
        if data[i] in Leagues:
            print()
            print(colored(data[i].upper(), 'blue'))
            print()
            i+=1
        elif ":" in data[i] or data[i] in stoppers or "mins" in data[i]:    #BBC sport outputs the time as "HH:MM" and minutes of a live game as "x mins"
            print("| " + data[i])
            print()
            i+=1
        elif len(data[i]) == 1:
            print(data[i], end=' ')
            i+=1
        else:
            print(data[i], end=' ')
            i+=1

            
#main program
chosen_date = date_function()
scraped_data = scraping(chosen_date)
cleaned_data = clean_data(scraped_data)
print_data(cleaned_data)