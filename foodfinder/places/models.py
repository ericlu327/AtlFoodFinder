# foodfinder/places/models.py

from django.db import models
from django.contrib.auth.models import User

class FoodPlace(models.Model):
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(null=True, blank=True)
    user_ratings_total = models.IntegerField(null=True, blank=True)
    cuisine_type = models.CharField(max_length=255, null=True, blank=True)
    opening_hours = models.JSONField(null=True, blank=True)
    photo_reference = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    food_place = models.ForeignKey(FoodPlace, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Review by {self.user.username} for {self.food_place.name}'
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_place = models.ForeignKey(FoodPlace, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'food_place') 
    def __str__(self):
        return f'{self.user.username} favorited {self.food_place.name}'