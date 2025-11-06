"""
Handle API calls to holiday database
"""
import requests
from datetime import datetime


def fetch_holidays(year=2025, country="BR"):
    """
    Fetch public holidays for a specific year and country
    API: https://date.nager.at/api/v3/PublicHolidays/{year}/{country}
    """
    try:
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            holidays_data = response.json()
            
            # Convert to dictionary for easier lookup
            # Format: {date: holiday_name}
            holidays = {}
            for holiday in holidays_data:
                date = holiday['date']  # Format: YYYY-MM-DD
                name = holiday['name']
                holidays[date] = name
            
            return holidays
        else:
            print(f"Error fetching holidays: {response.status_code}")
            return {}
            
    except Exception as e:
        print(f"Error connecting to holiday API: {e}")
        return {}


def check_if_holiday(date_obj, holidays):
    """
    Check if a given date is a holiday
    Returns: (is_holiday: bool, holiday_name: str)
    """
    # Format date as YYYY-MM-DD for comparison
    date_str = date_obj.strftime("%Y-%m-%d")
    
    if date_str in holidays:
        return True, holidays[date_str]
    else:
        return False, ""
