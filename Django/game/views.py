from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Card
from .serializers import CardSerializer

# Create your views here.

class PackOpenerView(APIView):
    def get(self, request):
        cards = Card.objects.order_by('?')[:7]
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)