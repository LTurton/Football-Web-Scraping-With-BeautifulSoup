import re
from fuzzywuzzy import fuzz

class LeaguesHandler:

    @staticmethod
    def all_leagues():    
        return ['Australian A-League',
            'Austrian Bundesliga',
            'Belgian First Division A',
            'Brazilian Série A',
            'Champions League',
            'Championship',
            'Cymru Premier',
            'Danish Superliga',
            'Dutch Eredivisie',
            'EFL Cup',
            'EFL Trophy',
            'Euro U21 Qualifying',
            'Europa Conference League',
            'Europa League',
            'FA Cup Qualifying',
            'Finnish Veikkausliiga',
            'French Ligue 1',
            'German Bundesliga',
            'Greek Superleague',
            'Highland League',
            'International Friendlies',
            'Irish Premier Division',
            'Irish Premiership',
            'Italian Serie A',
            'League One',
            'League Two',
            'Lowland League',
            'National League',
            'National League North',
            'National League South',
            'Norwegian Eliteserien',
            'Portuguese Primeira Liga',
            'Premier League',
            'Russian Premier League',
            'Scottish Challenge Cup',
            'Scottish Championship',
            'Scottish Cup',
            'Scottish Cup Qualifying',
            'Scottish League Cup',
            'Scottish League One',
            'Scottish League Two',
            'Scottish Premiership',
            "Scottish Women's Premier League 1",
            'Spanish La Liga',
            'Swedish Allsvenskan',
            'Swiss Super League',
            "The FA Women's Championship",
            "The FA Women's Super League",
            'Turkish Super Lig',
            'Under-21 Friendly',
            'United States Major League Soccer',
            'Welsh Cup',
            'Welsh League Cup',
            "Women's Champions League",
            "Africa Cup of Nations",
            "World Cup Qualifying - North/Central America",
            "World Cup Qualifying - Asia",
            "World Cup Qualifying - South America"]
        
    @staticmethod
    def interesting_leagues ():
        return ['Champions League',
        'Championship',   
        'EFL Cup',
        'EFL Trophy',
        'Europa Conference League',
        'Europa League',
        'FA Cup Qualifying',    
        'League One',
        'League Two',   
        'Premier League']
        
    @staticmethod
    def common_abbreviations():
        return {"Prem" : "Premier League",
                "PL" : "Premier League",
                "FA Cup" : "FA Cup Qualifying",
                "CL" : "Champions League",
                "UCL" : "Champions League",
                "Carabao Cup" : "EFL Cup",
                "League Cup" : "EFL Cup"}
        
        
    @staticmethod
    def check_input_league_is_understood(user_string):

        #Check if User Has Used A Common Known Abbreviation:
        if user_string in LeaguesHandler.common_abbreviations():
            return LeaguesHandler.common_abbreviations()[user_string]
        
        #Do We Have An Exact Match:                
        if user_string in LeaguesHandler.all_leagues():
            return user_string
        
        #Case Match:
        for league in LeaguesHandler.all_leagues():
            if re.search(fr"\b{user_string}\b", league, flags=re.IGNORECASE | re.MULTILINE):
                return league
                
        # Fuzzy matching (i.e account for typos, errant spaces etc)
        for league in LeaguesHandler.all_leagues():
            similarity = fuzz.ratio(user_string.lower(), league.lower())
            if similarity >= 80:  # Example threshold
                return league
            
        # If no match found, raise an error
        raise ValueError(f"'{user_string}' is not a known league.")
            
    @staticmethod
    def custom_league_choice():
        user_string = input("What league would you like to see? ")
        
        user_string = LeaguesHandler.check_input_league_is_understood(user_string)

        return user_string