#Third Party Includes:
import requests
from bs4 import BeautifulSoup

from leagues import LeaguesHandler

class GamesAndScoresScraper:
    @staticmethod
    def scrape_games_and_leagues(date):
        #Based on work by: https://github.com/stevoslates/Football-Web-Scraping-With-BeautifulSoup
    
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
        
    # Helper Function - Cleaning (Remove Data From Leagues I Want To Ignore):
    @staticmethod
    def remove_unwanted_leagues(data, leagues_of_interest = LeaguesHandler.interesting_leagues()):

        cleaned_data = []
        skip = False  # Flag to skip elements between "not useful" and "useful"

        for element in data:
            if element in LeaguesHandler.all_leagues():
                if element not in leagues_of_interest:
                    # Found a "not useful" element, set the skip flag
                    skip = True
                else:
                    # Found a "useful" element, reset the skip flag
                    skip = False
                    cleaned_data.append(element)
            elif not skip:
                # If not skipping, add the element to cleaned_data
                cleaned_data.append(element)

        return cleaned_data
    
    @staticmethod
    def clean_data(data, leagues_of_interest = LeaguesHandler.interesting_leagues()):
        #Based on work by: https://github.com/stevoslates/Football-Web-Scraping-With-BeautifulSoup
        
        #Check we understand the requested league before doing anymore work:
        leagues_of_interest = LeaguesHandler.check_input_league_is_understood(leagues_of_interest)
        
        #the data goes Home - Time - Away - ' '. As it expects a time but this is instead blank for games that haven't kicked off yet.
        #so below i switch the blank with the time and delete he original time. Also this makes it easier when printing out the data.    
        indicies = []
        for index, item in enumerate(data):
            if item == '':
                data[index] = data[index - 2]
                indicies.append(index - 2)
    
    
        for index in sorted(indicies, reverse=True):
            del data[index]
    
        data = ['TBC' if word == 'TBCTo be Confirmed' else word for word in data]
        
        #Customisation - Filter to requested leagues:
        cleaned_data = GamesAndScoresScraper.remove_unwanted_leagues(data, leagues_of_interest)
        
        return cleaned_data
    
    @staticmethod
    def print_data(data):

        i=0
        #these words are when i know to print a new line!
        stoppers = ["TBC","FT","HT","P","AET"]

        #only want to print a "vs" after the first team then stop it for the second, so use this to toggle.        
        while i < len(data):
            if data[i] in LeaguesHandler.interesting_leagues():
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