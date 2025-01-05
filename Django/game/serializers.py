from rest_framework import serializers
from .models import Cards, UserProfile

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'
class UserProfileSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many =True)
    class Meta:
        model = UserProfile
        fields = ['user', 'cards']
        # no other user details