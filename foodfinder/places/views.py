# places/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ReviewForm
from .models import FoodPlace, Review
from .utils import fetch_food_places
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from geopy.distance import geodesic
from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodPlace
from django.contrib.auth.decorators import login_required
from geopy.distance import geodesic
import json
from django.core.serializers.json import DjangoJSONEncoder

# Function to classify cuisine type based on keywords in restaurant name
import requests

def classify_cuisine_via_yelp(restaurant_name, latitude, longitude):
    api_key = 'Jy5RviWFz9lwowmFc5Y7I5_86rE-45S8XZpgDvp2PnPCH0-LGtl8PQwJ8Rqb6ZCxcfalApMhHuM8Omq1a_9goN5qX4z1Xs_nxVce3EJlUYHjVqfWcvpWV7LWCXz7ZnYx'
    url = 'https://api.yelp.com/v3/businesses/search'

    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    params = {
        'term': restaurant_name,
        'latitude': latitude,
        'longitude': longitude,
        'limit': 1
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['businesses']:
            categories = data['businesses'][0]['categories']
            cuisine_types = [category['title'] for category in categories]
            return ', '.join(cuisine_types)
        else:
            return 'Unknown'
    else:
        print(f"Error fetching cuisine type from Yelp: {response.status_code}, {response.text}")
        return 'Unknown'

# Modified index view to include cuisine classification based on name
def index(request):
    query = request.GET.get('q')
    cuisine = request.GET.get('cuisine')
    rating = request.GET.get('rating')
    distance = request.GET.get('distance')
    location = request.GET.get('location')

    # Fetch Google Places data
    if query:
        places_data = fetch_food_places(query=query)
    else:
        places_data = fetch_food_places()

    for place_data in places_data:
        place_id = place_data.get('place_id')
        if not place_id:
            continue

        # Check if the place already exists in the database
        try:
            place = FoodPlace.objects.get(place_id=place_id)
            if not place.cuisine_type or place.cuisine_type == 'Unknown':
                # If cuisine type is not available, classify using Yelp
                restaurant_name = place_data.get('name', '')
                latitude = place_data['geometry']['location']['lat']
                longitude = place_data['geometry']['location']['lng']
                
                # Get cuisine type from Yelp
                cuisine_type = classify_cuisine_via_yelp(restaurant_name, latitude, longitude)
                place.cuisine_type = cuisine_type
                place.save()
        except FoodPlace.DoesNotExist:
            # If the place does not exist in the database, add it
            restaurant_name = place_data.get('name', '')
            latitude = place_data['geometry']['location']['lat']
            longitude = place_data['geometry']['location']['lng']
            cuisine_type = classify_cuisine_via_yelp(restaurant_name, latitude, longitude)

            opening_hours = place_data.get('opening_hours', {})
            photo_reference = place_data.get('photos', [{}])[0].get('photo_reference')

            FoodPlace.objects.create(
                place_id=place_id,
                name=place_data.get('name'),
                address=place_data.get('formatted_address'),
                latitude=latitude,
                longitude=longitude,
                rating=place_data.get('rating'),
                user_ratings_total=place_data.get('user_ratings_total'),
                cuisine_type=cuisine_type,
                opening_hours=opening_hours,
                photo_reference=photo_reference,
            )

    # Filtering food places for display
    food_places = FoodPlace.objects.all()

    if query:
        food_places = food_places.filter(name__icontains=query)

    if cuisine:
        food_places = food_places.filter(cuisine_type__icontains=cuisine)

    if rating:
        food_places = food_places.filter(rating__gte=float(rating))

    if location and distance:
        user_lat, user_lng = map(float, location.split(','))
        user_location = (user_lat, user_lng)

        filtered_food_places = []
        for place in food_places:
            place_location = (place.latitude, place.longitude)
            distance_to_place = geodesic(user_location, place_location).km

            if distance_to_place <= float(distance):
                filtered_food_places.append(place)

        food_places = filtered_food_places

    food_places_list = list(food_places.values(
        'name', 'address', 'latitude', 'longitude', 'cuisine_type', 'rating', 'user_ratings_total', 'opening_hours'
    ))
    food_places_json = json.dumps(food_places_list, cls=DjangoJSONEncoder)

    context = {
        'food_places': food_places,
        'food_places_json': food_places_json,
        'query': query,
        'cuisine': cuisine,
        'rating': rating,
        'distance': distance,
    }
    return render(request, 'places/index.html', context)

def food_place_detail(request, pk):
    food_place = get_object_or_404(FoodPlace, pk=pk)
    reviews = food_place.reviews.all()
    return render(request, 'places/food_place_detail.html', {'food_place': food_place, 'reviews': reviews})

@login_required
def add_review(request, pk):
    food_place = get_object_or_404(FoodPlace, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.food_place = food_place
            review.user = request.user
            review.save()
            return redirect('food_place_detail', pk=food_place.pk)
    else:
        form = ReviewForm()
    return render(request, 'places/add_review.html', {'form': form, 'food_place': food_place})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
