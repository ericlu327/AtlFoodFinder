# places/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ReviewForm
from .models import FoodPlace, Review
from .utils import fetch_food_places
import json
from django.core.serializers.json import DjangoJSONEncoder

def index(request):
    query = request.GET.get('q')
    if query:
        places_data = fetch_food_places(query=query)
    else:
        places_data = fetch_food_places()

    for place_data in places_data: # This is where we probaably need to fix cuisine data it's not being displayed properly.
        opening_hours = place_data.get('opening_hours', {})
        types = place_data.get('types', [])
        cuisine = ', '.join(types)
        photo_reference = None
        if 'photos' in place_data:
            photo_reference = place_data['photos'][0]['photo_reference']

        place_id = place_data.get('place_id')
        if not place_id:
            continue

        place, created = FoodPlace.objects.update_or_create(
            place_id=place_id,
            defaults={
                'name': place_data.get('name'),
                'address': place_data.get('formatted_address'),
                'latitude': place_data['geometry']['location']['lat'],
                'longitude': place_data['geometry']['location']['lng'],
                'rating': place_data.get('rating'),
                'user_ratings_total': place_data.get('user_ratings_total'),
                'cuisine_type': cuisine,
                'opening_hours': opening_hours,
                'photo_reference': photo_reference,
            }
        )

    if query:
        food_places = FoodPlace.objects.filter(name__icontains=query)
    else:
        food_places = FoodPlace.objects.all()

    food_places_list = list(food_places.values(
        'name', 'address', 'latitude', 'longitude', 'cuisine_type', 'rating', 'user_ratings_total', 'opening_hours'
    ))
    food_places_json = json.dumps(food_places_list, cls=DjangoJSONEncoder)

    context = {
        'food_places': food_places,
        'food_places_json': food_places_json,
        'query': query,
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
