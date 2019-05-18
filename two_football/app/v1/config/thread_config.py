import requests
from datetime import datetime, timedelta
import json

POOL_TIME = 20

ACTION = 'get_events'
API_KEY = 'c28fc9ce3a86c54192c02d126d270802bb06d625cf0db3d459415ef7b025c280'


def fetch3rdAPI(league_id):

    today = datetime.now()
    from_date = today - timedelta(days=3)
    to_date = today + timedelta(days=8)

    from_date_str = from_date.strftime('%y-%m-%d')
    to_date_str = to_date.strftime('%y-%m-%d')

    params = (('action', ACTION),
              ('from', from_date_str),
              ('to', to_date_str),
              ('league_id', league_id),
              ('APIkey', API_KEY))

    # bytes
    content = requests.get('https://apifootball.com/api/', params=params).content

    # list
    match_list = json.loads(content.decode('utf8'))

    # when no events, result is object
    if type(match_list) is not list:
        return None

    return match_list

