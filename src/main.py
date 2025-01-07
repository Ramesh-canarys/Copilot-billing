import requests
import csv
from urllib.parse import urlparse, parse_qs
from datetime import datetime, tzinfo, timedelta
from calendar import monthrange
from dateutil import parser

# Global constants
ENTERPRISE_SLUG = ''  # your_enterprise_slug_here
AUTH_TOKEN = ''  # your_auth_token_here

class tzoffset(tzinfo):
    def __init__(self, name, offset):
        self.offset = offset
        self.name = name

    def utcoffset(self, dt):
        return timedelta(seconds=self.offset)

    def tzname(self, dt):
        return self.name

    def dst(self, dt):
        return timedelta(0)

def get_copilot_billing_seats():
    seats_info = []
    try:
        api_url = f"https://api.github.com/enterprises/{ENTERPRISE_SLUG}/copilot/billing/seats"
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

        while api_url:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                seats_info.extend([
                    {
                        'login': item.get('assignee', {}).get('login'),
                        'last_activity_at': item.get('last_activity_at'),
                        'created_at': item.get('created_at'),
                        'seat': item.get('id'),
                        'team': item.get('assigning_team', {}).get('name')
                    }
                    for item in data['seats']
                    if item.get('assignee')
                ])
                link_header = response.headers.get('Link', None)
                if link_header:
                    next_page = None
                    links = link_header.split(',')
                    for link in links:
                        if 'rel="next"' in link:
                            next_page = link.split(';')[0].strip('<> ')
                            break
                    api_url = next_page
                else:
                    break
            else:
                print(f"Error: Received response code {response.status_code}")
                break
    except Exception as e:
        print(f"An error occurred: {e}")

    return seats_info

def calculate_daily_rate():
    current_date = datetime.now()
    days_in_month = monthrange(current_date.year, current_date.month)[1]
    daily_rate = 19 / days_in_month
    return daily_rate

def calculate_billing(seats_info):
    daily_rate = calculate_daily_rate()
    try:
        for seat in seats_info:
            if seat['created_at']:
                last_activity_date = datetime.now().astimezone(tzoffset('None', 19800))
                created_date = parser.parse(seat['created_at'])
                days_active = (last_activity_date - created_date).days + 1
                daily_rate = round(daily_rate, 3)
                seat['number_of_active_days'] = days_active
                seat['per_day_rate'] = daily_rate
                seat['bill'] = round(days_active * daily_rate, 2)
            else:
                seat['bill'] = 0.0
    except Exception as e:
        print(f"An error occurred while calculating billing: {e}")
    return seats_info

def write_to_csv(seats_info):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'copilot_seats_info_{timestamp}.csv'
    try:
        with open(filename, 'w', newline='') as file:
            fieldnames = ['login', 'last_activity_at', 'created_at', 'seat', 'team', 'number_of_active_days', 'per_day_rate', 'bill']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for seat in seats_info:
                writer.writerow(seat)
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

if __name__ == "__main__":
    try:
        seats_info = get_copilot_billing_seats()
        if isinstance(seats_info, list):
            seats_info = calculate_billing(seats_info)
            write_to_csv(seats_info)
            print(f"Data written to file. Total seats: {len(seats_info)}")
        else:
            print(seats_info)
    except Exception as e:
        print(f"An error occurred in the main execution: {e}")