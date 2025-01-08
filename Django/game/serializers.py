from rest_framework import serializers
from .models import Card, UserProfile, DeckCard, UserDeck

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
class UserProfileSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many =True)
    class Meta:
        model = UserProfile
        fields = ['user', 'cards']
        # no other user details
        
class DeckCardSerializer(serializers.ModelSerializer):
    card_name = serializers.CharField(source='card.name', read_only=True)
    card_image = serializers.ImageField(source='card.image', read_only=True)
    
    class Meta:
        model = DeckCard
        fields = ['card', 'name', 'image', 'count']
        
class UserDeckSerializer(serializers.ModelSerializer):
    cards = DeckCardSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserDeck
        fields = ['id', 'name', 'user', 'cards']
        