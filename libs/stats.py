import bs4 as bs
import requests
import libs.text_utils as tu

BASE_URL = 'https://github.com/users/<USERNAME>/contributions'

def get_contribution(username):
    url = BASE_URL.replace('<USERNAME>', username)
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    
    summary = soup.find('h2', class_='f4 text-normal mb-2').text
    summary = tu.standardize_text(summary)
    
    data = {}
    
    table = soup.find('table', class_='ContributionCalendar-grid')
    info_rows = table.find_all('tr', {'style': 'height: 10px'})
    
    for row in info_rows:
        weekday_label = row.find('td', class_='ContributionCalendar-label').find('span').text
        
        for i in row.find_all('td', class_='ContributionCalendar-day'):
            date = i.get('data-date')
            level = i.get('data-level')
            data[date] = int(level)
        
    return {
        'username': username,
        'title': 'Github Contribution',
        'summary': summary,
        'data': data
    }
    