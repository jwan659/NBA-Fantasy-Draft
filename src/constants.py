import os

DATA_DIR = os.path.join(os.getcwd().replace('/src', ''), 'data')

# Scraping
SECONDS_SLEEP = 1

# Plotly Credentials
PLOTLY_USERNAME = 'your_username'
PLOTLY_API_KEY = 'your_api_key'

SEASONS = [2015,2016,2017,2018,2019,2020,2021]

TEAMS  = ['ATL','BKN','BOS','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']

# Data for DraftKings is not available prior to 2014-15
# https://en.wikipedia.org/wiki/2018-2019_NBA_season
# TODO: automatically extract season start and end dates from wikipedia
DF_VARIABLES = ['Name', 'Date', 'Team',  'FPTS', 'Home', 'W', 'W_PTS', 'L', 'L_PTS', 'MP',
                'FG', 'FGA', 'FG_perc', '3P', '3PA', '3P_perc', 'FT', 'FTA', 'FT_perc',
                'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'DD', 'TD',
                'USG_perc', 'DRtg', 'ORtg', 'AST_perc', 'DRB_perc', 'ORB_perc', 'BLK_perc',
                'TOV_perc', 'STL_perc', 'eFG_perc']

DF_FEATURES = ['Date', 'Name', 'Team', 'Pos', 'FPTS', 'Salary',
               # Additional Features
               'Starter', 'Rest', 'Rota_All', 'Rota_Pos', 'Home',
               'PG', 'SG', 'F', 'C', 'Value', 'FPTS_std',
               # Basic Stats with weighted mean
               'PTS', '3P',  'AST', 'TRB',
               'STL', 'BLK', 'TOV', 'DD', 'TD',
               # Additional Stats with weighted mean
               'MP', 'FT', 'FTA', 'FGA', '3PA', 'DRB', 'ORB',
               # Advanced Stats with weighted mean
               'USG_perc', 'DRtg', 'ORtg', 'AST_perc', 'DRB_perc', 'ORB_perc',
               'BLK_perc', 'TOV_perc', 'STL_perc', 'eFG_perc', 'FG_perc', '3P_perc', 'FT_perc']