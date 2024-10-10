import os
import logging

Client_ID = os.environ.get('Client_ID')
Client_Secrect = os.environ.get('Client_Secret')
DynamoDB_Table = os.environ.get("DynamoDB_Table")
BASE_URL = os.environ.get('BASE_URL')

LOGIN_CALLBACK_URL = BASE_URL + "/callback"

# yahoo urls
AUTHORIZE_URL="https://api.login.yahoo.com/oauth2/request_auth"
ACCESS_TOKEN_URL="https://api.login.yahoo.com/oauth2/get_token"
FANTASY_API_URL = "https://fantasysports.yahooapis.com/fantasy/v2"


# project root directory
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# This font file is used to support Chinese in chart
CHINESE_FONT_FILE = os.path.join(PROJECT_ROOT, 'SimSun-01.ttf')


logger = logging.getLogger()
logger.setLevel(logging.INFO)



