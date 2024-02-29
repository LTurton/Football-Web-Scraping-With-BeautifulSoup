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
            "The FA Cup",
            "The FA Women's Championship",
            "The FA Women's Super League",
            'Turkish Super Lig',
            'Under-21 Friendly',
            'United States Major League Soccer',
            "UEFA Women's Nations League"
            'Welsh Cup',
            'Welsh League Cup',
            "Women's Champions League",
            "Africa Cup of Nations",
            "Women's International Friendlies",
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
        return {"prem" : "Premier League",
                "pl" : "Premier League",
                "fa cup" : "The FA Cup",                
                "cl" : "Champions League",
                "ucl" : "Champions League",
                "carabao cup" : "EFL Cup",
                "league cup" : "EFL Cup"}
     
    @staticmethod    
    def find_closest_match(user_string):
        # Fuzzy matching (i.e account for typos, errant spaces etc)
        max_similarity = 0
        closest_match = None

        for league in LeaguesHandler.all_leagues():
            similarity = fuzz.ratio(user_string.lower(), league.lower())
            if similarity > max_similarity:
                max_similarity = similarity
                closest_match = league

        if max_similarity >= 80:  # Example threshold
            return closest_match
        else:
            return None

    @staticmethod
    def _is_league_known(user_string):

        #Check if User Has Used A Common Known Abbreviation:
        if user_string in LeaguesHandler.common_abbreviations():
            return LeaguesHandler.common_abbreviations()[user_string.lower()]
        
        #Do We Have An Exact Match:                
        if user_string in LeaguesHandler.all_leagues():
            return user_string
        
        #Case Match:
        for league in LeaguesHandler.all_leagues():
            if re.search(fr"\b{user_string}\b", league, flags=re.IGNORECASE | re.MULTILINE):
                return league
          
        #Fuzzy Logic Near      
        best_match = LeaguesHandler.find_closest_match(user_string)
        if best_match is not None:
            return best_match
            
        # If no match found, raise an error
        raise ValueError(f"'{user_string}' is not a known league.")
            
    @staticmethod
    def custom_league_choice():
        user_string = input("What league would you like to see? ")        
        user_string = LeaguesHandler._is_league_known(user_string)
        return user_string
    
    @staticmethod
    def filter_input_leagues(leagues_of_interest):
        #Filters Leagues Provided By A User:
                
        # Assuming 'leagues_of_interest' is either a list or a single value
        checked_leagues_of_interest = []
        if isinstance(leagues_of_interest, list):
            for league in leagues_of_interest:
                try:
                    checked_league = LeaguesHandler._is_league_known(league)
                    checked_leagues_of_interest.append(checked_league)
                except ValueError as ve:
                    print(f"{ve}")
        else:
            try:
                checked_league = LeaguesHandler._is_league_known(leagues_of_interest)
                checked_leagues_of_interest.append(checked_league)
            except ValueError as ve:
                print(f"{ve}")

        if not checked_leagues_of_interest:            
            raise ValueError("We couldn't interpret the requested league(s).")

        return checked_leagues_of_interest