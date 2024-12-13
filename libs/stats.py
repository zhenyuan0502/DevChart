import bs4 as bs
import requests
import libs.text_utils as tu
from datetime import datetime, timedelta

GITHUB_BASE_URL = 'https://github.com/users/<USERNAME>/contributions'
LEETCODE_BASE_URL = 'https://leetcode.com/graphql/'

def get_data_template():
    """
    Create a data template with today's date and the date 366 days ago.

    Returns:
        dict: A dictionary with today's date and the date 366 days ago as keys, both initialized to 0.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    last_366_days = (datetime.now() - timedelta(days=366)).strftime('%Y-%m-%d')    
    data = {}
    data[today] = 0
    data[last_366_days] = 0
    return data

def get_github_contribution(username):
    """
    Fetch GitHub contribution data for a given username.

    Args:
        username (str): GitHub username.

    Returns:
        dict: A dictionary containing the username, title, summary, and contribution data.
    """
    url = GITHUB_BASE_URL.replace('<USERNAME>', username)
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    
    summary = soup.find('h2', class_='f4 text-normal mb-2').text
    summary = tu.standardize_text(summary)
    
    data = get_data_template()
    
    table = soup.find('table', class_='ContributionCalendar-grid')
    
    for i in table.find_all('td', class_='ContributionCalendar-day'):
        date = i.get('data-date')
        level = i.get('data-level')
        data[date] = int(level)
        
    return {
        'username': username,
        'title': 'Github Contribution',
        'summary': f'GitHub with {summary}',
        'data': data
    }

import json
def get_leetcode_submission(username):
    """
    Fetch LeetCode submission data for a given username.

    Args:
        username (str): LeetCode username.

    Returns:
        dict: A dictionary containing the username, title, summary, and submission data.
    """
    response = requests.post(LEETCODE_BASE_URL, json={
        'operationName': 'userProfileCalendar',
        'query': "\n    query userProfileCalendar($username: String!, $year: Int) {\n  matchedUser(username: $username) {\n    userCalendar(year: $year) {\n      activeYears\n      streak\n      totalActiveDays\n      dccBadges {\n        timestamp\n        badge {\n          name\n          icon\n        }\n      }\n      submissionCalendar\n    }\n  }\n}\n    ",
        'variables': {
            'username': username,
        }
    })
    
    data = get_data_template()
    sum = 0
    
    response_data = response.json()
    if 'errors' in response_data:
        return {
            'username': username,
            'title': 'LeetCode Submission',
            'summary': f'LeetCode with {sum} submissions in past one year',
            'data': data
        }
        
    user = response_data['data']['matchedUser']['userCalendar']
    submissions = json.loads(user['submissionCalendar'])
    
    for key, val in submissions.items():
        date = tu.unixtimestamp_to_date(key)
        data[date] = val
        sum += val
    
    return {
        'username': username,
        'title': 'LeetCode Submission',
        'summary': f'LeetCode with {sum} submissions in past one year',
        'data': data
    }
