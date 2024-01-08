"""
1. run script every day 23:50 
2. if there is an action on that day than take that one and add it to duration & pace and also the link from that run
3. add it to the cell of the respective data 

"""
import requests
from dotenv import load_dotenv
from datetime import date, datetime
import os

load_dotenv()  # take environment variables from .env.
access_token = os.getenv('access_token')

def main():
    """
    main function
    """
    activities=strava()
    #print("activities")
    #print(activities)
    date=get_date()
    daily_action=get_daily_action_from_strava(activities, date)
    print(daily_action)
    # for activity in activities:
    #     #print(activity)
    #     print(datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'))
    #     break
    #     #print(activity['start_date_local'])

def strava():
    """
    gets data from strava
    """
    response = requests.get('https://www.strava.com/api/v3/athlete/activities', headers={'Authorization': f'Bearer {access_token}'})
    return response.json()

def get_date():
    """
    gets the date from the google sheet
    """
    today = date.today()
    return today.strftime("%Y-%m-%d")

def get_daily_action_from_strava(activities, date):
    """
    gets the daily action from strava
    """
    # date = "2023-10-04"
    daily_activity = None
    for activity in activities:
        if datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d') == date:
            daily_activity = activity
            break
    return daily_activity

def get_daily_action():
    """
    gets the daily action from the google sheet
    """
    pass

def get_duration():
    """
    gets the duration from strava
    """
    pass

def get_pace():
    """
    gets the pace from strava
    """
    pass

def write_duration_to_sheet():
    """
    writes the duration data to the google sheet
    """
    pass

def write_pace_to_sheet():
    """
    writes the pace data to the google sheet
    """
    pass

def write_link_to_sheet():
    """
    writes the link to the run to the google sheet
    """
    pass


if __name__ == "__main__":
    main()

#https://www.strava.com/oauth/authorize?client_id=119488&redirect_uri=http://localhost:8000&response_type=code&scope=activity:read_all

#http://localhost:8000/?state=&code=65cff7e81cc8ace8deb4832cb3f7a664d75efefe&scope=read,activity:write