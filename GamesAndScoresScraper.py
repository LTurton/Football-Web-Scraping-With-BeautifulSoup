#Third Party Includes:
import requests
from bs4 import BeautifulSoup
from termcolor import colored

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
        all_leagues = LeaguesHandler.all_leagues()
        cleaned_data = []
        keep = False  
        
        #Handle Single String Inputs:
        if isinstance(leagues_of_interest, str):
            leagues_of_interest = [leagues_of_interest]        

        for element in data:
            if element in leagues_of_interest:
                keep = True
            elif element in all_leagues and element not in leagues_of_interest:
                keep = False

            if keep or element in leagues_of_interest:
                cleaned_data.append(element)

        if not cleaned_data:
                print("No Data found for the requested league, check your inputs.")

        return cleaned_data
    
    @staticmethod
    def clean_data(data, leagues_of_interest = LeaguesHandler.interesting_leagues()):
        #Based on work by: https://github.com/stevoslates/Football-Web-Scraping-With-BeautifulSoup
        
        #Check we understand the requested league before doing any work:
        checked_leagues_of_interest = LeaguesHandler.filter_input_leagues(leagues_of_interest)         
        
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
        cleaned_data = GamesAndScoresScraper.remove_unwanted_leagues(data, checked_leagues_of_interest)
        
        return cleaned_data
    
    @staticmethod
    def print_data(data):

        i=0
        #these words are when i know to print a new line!
        stoppers = ["TBC","FT","HT","P","AET"]

        #only want to print a "vs" after the first team then stop it for the second, so use this to toggle.        
        while i < len(data):
            if data[i] in LeaguesHandler.all_leagues():
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