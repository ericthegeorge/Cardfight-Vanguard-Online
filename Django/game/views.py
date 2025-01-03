from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cards
from game.serializers import CardSerializer
from random import sample

# Create your views here.

class PackOpenerView(APIView):
    def get(self, request):
        card_ids = list(Cards.objects.values_list('id', flat=True))
        random_ids = sample(card_ids, 7)
        cards = Cards.objects.filter(id__in=random_ids)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
class AllCardsView(APIView):
    def get(self, request):
        cards = Cards.objects.all()
        
        card_data = []
        for card in cards:
            card_data.append({
                'name': card.name,
                'rarity': card.rarity,
            })
            
        return Response(card_data)