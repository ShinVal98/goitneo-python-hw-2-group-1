from collections import defaultdict
from datetime import datetime, timedelta
from exc_3 import * 

def get_birthdays_per_week(users):
    birthdays_by_day = defaultdict(list)
    today = datetime.today().date()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    current_weekday = today.weekday()
    start_of_week = (today - timedelta(days=current_weekday))
 
    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=birthday_this_year.year + 1)
        
        delta_days = (birthday_this_year - today).days
        
        if 0 <= delta_days < 7:
            day_of_week = (today.weekday() + delta_days) % 7
            
            if start_of_week <= birthday_this_year <= start_of_week + timedelta(days=6):
                birthdays_by_day[weekdays[day_of_week]].append(name)
    
    result = dict(birthdays_by_day)

    sorted_result = {day: result[day] for day in sorted(result, key=lambda x: weekdays.index(x))}
    return sorted_result