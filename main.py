import requests
from dotenv import load_dotenv
from datetime import date, datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()  
access_token = os.getenv('access_token')

def main():
    """
    main function
    """
    activities=strava()
    date=get_date()
    daily_action=get_daily_action_from_strava(activities, date)
    duration=get_duration_from_strava(daily_action)
    duration_in_minutes=convert_to_minutes(duration)
    speed = get_pace_from_strava(daily_action)
    link = get_link_from_strava(daily_action)
    write_duration_and_pace_to_sheet(date, duration_in_minutes, speed, link)

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
    daily_activity = None
    for activity in activities:
        if datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d') == date:
            daily_activity = activity
            break
    return daily_activity

def get_duration_from_strava(daily_activity):
    """
    gets the duration from strava
    """
    return daily_activity['moving_time']

def convert_to_minutes(duration):
    """
    converts the duration to minutes
    """
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes}.{seconds}"

def get_pace_from_strava(daily_activity):
    """
    gets the pace from strava and converts it to minutes per kilometer
    """
    # Strava's average_speed is in meters per second
    average_speed_mps = daily_activity['average_speed']
    # Convert speed to pace (minutes per kilometer)
    if average_speed_mps > 0:  # To avoid division by zero
        pace_seconds_per_km = 1000 / average_speed_mps  # seconds per kilometer
        pace_minutes_per_km = pace_seconds_per_km / 60  # minutes per kilometer
        # Format the pace into minutes and seconds per kilometer
        pace_minutes = int(pace_minutes_per_km)
        pace_seconds = int((pace_minutes_per_km - pace_minutes) * 60)
        return f"{pace_minutes}:{pace_seconds:02d}"
    
def get_link_from_strava(daily_activity):
    """
    gets the link from strava
    """
    return daily_activity['external_id']

def write_duration_and_pace_to_sheet(date, duration, pace):
    """
    writes the duration data to the google sheet
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('lean_fit').sheet1
    first_row_values = sheet.col_values(1)
    column_index = first_row_values.index(formatted_date) + 1 
    sheet.update_cell(column_index, 5, duration)
    sheet.update_cell(column_index, 6, pace)

