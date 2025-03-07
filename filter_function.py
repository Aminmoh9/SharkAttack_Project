import re
from datetime import datetime

def extract_month(date):
    date = re.sub(r'^\W+|\W+$', '', date)

    formats = [
        '%d %b %Y', '%d-%b-%Y', '%b %Y', '%d-%B-%Y', '%B %Y',
        '%Y-%m-%d', '%Y/%m/%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y', '%m/%d/%Y',
        '%B %d, %Y', '%b %d, %Y', '%d %B %Y', '%Y %b %d', '%Y %d %b', '%d %B %Y %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%d %b-%Y', '%d-%B %Y', '%B %Y', '%Y.%m.%d', '%d-%b-%Y', '%b-%Y', '%d%b%Y', '%Y', '%B %Y', '%d-%B-%Y', '%b%Y',
        '%B %Y', '%b %Y', '%d-%B-%Y', '%d-%b-%Y', '%B %Y', '%b %Y'
    ]

    seasons = {
        'winter': 13, 'spring': 14, 'summer': 15, 'fall': 16,
    }

    # Handle double hyphens
    date = date.replace("--", "-")

    # Handle "Nox"
    date = date.replace("Nox", "Nov")

    # Handle "3rd", "2nd", "1st", "4th"
    date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date)

    # Handle "MonYYYY"
    date = re.sub(r'([A-Za-z]{3})(\d{4})', r'\1-\2', date)

    # Handle "DD-MonYYYY"
    date = re.sub(r'(\d{2})([A-Za-z]{3})(\d{4})', r'\1-\2-\3', date)

    # Handle "Circa"
    date = date.replace("Circa ", "")

    # Handle "Early summer"
    date = date.replace("Early ", "")

    # Handle "t937", "p1896"
    date = re.sub(r'([A-Za-z]{3}-\d{3})[tp]', r'\1', date)

    # Handle "Reported"
    date = date.replace("Reported ", "")
    
    # Handle "Ap" as "Apr"
    date = date.replace("Ap-", "Apr-")
    date = date.replace("Ap ", "Apr ")
    date = date.replace("July", "Jul")
    date = date.replace("Sept", "Sep")
    date = date.replace("March", "Mar")
    
    # Check for seasons
    for season, month_num in seasons.items():
        if season in date.lower():
            return month_num

    # Check for year only
    if re.fullmatch(r'\d{4}', date):
        return 0

    # Find the first date
    date_match = re.search(r'\d{1,2}-[A-Za-z]{3}-\d{4}|\d{1,2}\s[A-Za-z]{3}\s\d{4}|[A-Za-z]{3}-\d{4}|[A-Za-z]{3}\s\d{4}|\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}|\d{1,2}\s[A-Za-z]{3}-\d{4}|\d{4}\.\d{2}\.\d{2}|\d{4}|\d{1,2}[A-Za-z]{3}\d{4}|[A-Za-z]{3}\d{4}|[A-Za-z]+\s\d{4}|[A-Za-z]+-\d{4}|\d{1,2}-[A-Za-z]+-\d{3}|\d{1,2}-[A-Za-z]{3}-\d{3}', date)
    if date_match:
        date = date_match.group(0)
    else:
        return 0

    for fmt in formats:
        try:
            date_obj = datetime.strptime(date, fmt)
            return date_obj.month
        except ValueError:
            continue
    
    # Handle 3-digit year
    date_match = re.search(r'\d{1,2}-[A-Za-z]{3}-\d{3}', date)
    if date_match:
        date_str = date_match.group(0)
        day, month, year = date_str.split('-')
        year = "1" + year
        try:
            date_obj = datetime.strptime(f"{day}-{month}-{year}", "%d-%b-%Y")
            return date_obj.month
        except ValueError:
            return 0
    
    return 0





def month_to_season(month):
    if month in [12, 1, 2, 13]:
        return "Winter"
    elif month in [3, 4, 5, 14]:
        return "Spring"
    elif month in [6, 7, 8, 15]:
        return "Summer"
    elif month in [9, 10, 11, 16]:
        return "Fall"
    else:
        return "Unknown"

    #Creating function for categorizing the activity-Amin
def categorize_activity(activity):
    activity = str(activity).lower()  # Ensuring activity is a string and lowercase
    
    if 'swim' in activity or 'wad' in activity or 'bath' in activity or "stand" in activity or "walk" in activity:
        return 'swimming'
    elif 'surf' in activity or "body board" in activity or "boogie board" in activity or "float" in activity or "treading water" in activity or "foil boarding" in activity:
        return 'surfing'
    elif 'fish' in activity or 'spearfish' in activity:
        return 'fishing'
    elif 'diving' in activity or 'snorkel' in activity:
        return 'diving'
    elif 'boat' in activity or "kayak" in activity or "canoe" in activity or "fell overboard" in activity or "paddl" in activity or "row" in activity:
        return 'watercraft'
    elif "unknown" in activity:
        return "unknown"
    else:
        return "other activities"