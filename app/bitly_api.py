import requests
from collections import defaultdict

BASE_URL = 'https://api-ssl.bitly.com/v4'

def headers(access_token):
    return {'Authorization': f"Bearer {access_token}"}


def user_info(access_token):
    USER_URL = BASE_URL + '/user'
    response = requests.get(USER_URL, headers=headers(access_token))
    return response.json()


def group_info(access_token):
    group_guid = user_info(access_token)['default_group_guid']
    BITLINKS_BY_GROUP_URL = BASE_URL + f'/groups/{group_guid}/bitlinks'
    response = requests.get(BITLINKS_BY_GROUP_URL, headers=headers(access_token))
    return response.json()


def average_clicks(country_data):
    return round(
        sum(country_data)/len(country_data))


def average_clicks_per_country(access_token):
    countries = defaultdict(list)
    for link in group_info(access_token)['links']:
        bitlink = link['id']
        DATA_BY_COUNTRY = BASE_URL + f'/bitlinks/{bitlink}/countries?units=30'
        response = requests.get(DATA_BY_COUNTRY, headers=headers(access_token))
        
        for country_data in response.json()['metrics']:
            countries[country_data['value']].append(country_data['clicks'])
    
    avg_clicks_per_country = [
        {
            'value': country,
            'average_clicks': average_clicks(countries[country])
        } 
        for country in countries
    ]

    return {'facet':'countries', 'metrics':avg_clicks_per_country}
