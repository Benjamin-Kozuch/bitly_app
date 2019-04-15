import requests
from collections import defaultdict

BASE_URL = 'https://api-ssl.bitly.com/v4'

def headers(access_token):
    return {'Authorization': f"Bearer {access_token}"}


def user_info(access_token):
    USER_URL = f'{BASE_URL}/user'
    response = requests.get(USER_URL, headers=headers(access_token))
    return response.json()


def group_info(access_token):
    group_guid = user_info(access_token)['default_group_guid']
    BITLINKS_BY_GROUP_URL = f'{BASE_URL}/groups/{group_guid}/bitlinks'
    response = requests.get(BITLINKS_BY_GROUP_URL, headers=headers(access_token))
    return response.json()


def average_clicks(country_data):
    return round(
        sum(country_data)/len(country_data))


def average_clicks_per_country(access_token, links=None):
    countries = defaultdict(list)
    for link in group_info(access_token)['links']:
        bitlink = link['id']
        DATA_BY_COUNTRY = f'{BASE_URL}/bitlinks/{bitlink}/countries?units=30'
        response = requests.get(DATA_BY_COUNTRY, headers=headers(access_token))
        
        for country_data in response.json()['metrics']:
            countries[country_data['value']].append(country_data['clicks'])
    
    avg_clicks_per_country = create_avg_click_list(countries)
    
    return {'facet':'countries', 'metrics':avg_clicks_per_country}


def create_avg_click_list(countries):
    return [
        {
            'value': country,
            'average_clicks': average_clicks(countries[country])
        } 
        for country in countries
    ]

