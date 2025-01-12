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
    card_image = serializers.CharField(source='card.image', read_only=True)
    
    class Meta:
        model = DeckCard
        fields = ['card', 'name', 'image', 'count']
        
class UserDeckSerializer(serializers.ModelSerializer):
    cards = DeckCardSerializer(many=True, read_only=True)
    user_profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = UserDeck
        fields = ['id', 'name', 'user_profile', 'cards']  # Replaced 'user' with 'user_profile'

    def validate_deck_cards(self, value):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or not hasattr(request.user, 'userprofile'):
            raise serializers.ValidationError("from context request, no user or user profile")
        user_profile = request.user.userprofile
        owned_cards = {card.id: card.count for card in user_profile.cards.all()}
        for deck_card in value:
            card_id = deck_card['card'].id  
            required_count = deck_card['count']      
        
            if card_id not in owned_cards:
                raise serializers.ValidationError("card not owned")
            if required_count > owned_cards[card_id]:
                raise serializers.ValidationError(f"not enough copies of card {card_id}. Need {required_count}, have {owned_cards[card_id]}")
            
        return value 

    def create(self, validated_data):
        deck_cards_data = validated_data.pop('deck_cards', [])
        user_deck = UserDeck.objects.create(**validated_data)
        
        for deck_card in deck_cards_data:
            DeckCard.objects.create(deck=user_deck, **deck_card)
        
        return user_deck

    def update(self, instance, validated_data):
        deck_cards_data = validated_data.pop('deck_cards', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        
        instance.deck_cards.all().delete()
        for deck_card in deck_cards_data:
            DeckCard.objects.create(deck=instance, **deck_card)
            
        return instance
