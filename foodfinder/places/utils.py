# foodfinder/places/utils.py

import requests

def fetch_food_places(query=None):
    api_key = 'AIzaSyDKQS3lLxpPb-qaJVGbpC8fiAoCFSNeiJg'  # Replace with your Google API key
    endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    params = {
        'query': query if query else 'restaurants in Atlanta',
        'key': api_key,
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'OK':
            return data.get('results', [])
        else:
            # Handle API error messages
            return []
    else:
        # Log the error or handle it appropriately
        return []
