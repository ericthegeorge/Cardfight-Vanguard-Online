from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate

from .models import Cards, UserProfile, UserCard
from game.serializers import CardSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from game.models import UserProfile

from random import sample
import random
SUPER_PACK_CHANCE = 0.5 # out of 100 in uniform random distribution
# Create your views here.

# DEBUG
# user = User.objects.create_user(username="testuser", password="1234")
# cards = Cards.objects.filter(rarity= "RRR", number__startswith="BT01")
# card1 = cards[0]
# card2 = cards[1]

# user_profile = UserProfile.objects.create(user=user)
# user_profile.cards.add(card1, card2)


# CHECK VALS
# test_user_cards = user_profile.cards.all()
# print(test_user_cards)

# END

class PackOpenerView(APIView):
    @staticmethod
    def choose_pack_rarities():
        pack_rarities = []
        super_pack_rarity = random.uniform(0, 100)
        if(super_pack_rarity < SUPER_PACK_CHANCE):
            # print("SUPER PACK GET!")
            # all cards are R or higher, and the last card is a RRR or higher
            for i in range (0, 6):
                rarity = random.uniform(0,100)
                card_rarity = -1
                match rarity:
                    case x if x < 45:
                        card_rarity = 'R'
                    case x if x < 85:
                        card_rarity = 'RR'
                    case _:
                        card_rarity = 'RRR'
                pack_rarities.append(card_rarity)
            rarity = random.uniform(0, 100)
            card_rarity = 'RRR'
            pack_rarities.append(card_rarity)
            return pack_rarities
        else:
            # first four cards 90 % chance to be common
            for i in range (0, 4):
                rarity = random.uniform(0,100)
                card_rarity = -1
                match rarity:
                    case x if x < 92:
                        card_rarity = 'C'
                    case x if x < 97:
                        card_rarity = 'R'
                    case x if x < 99:
                        card_rarity = 'RR'
                    case _:
                        card_rarity = 'RRR'
                pack_rarities.append(card_rarity)
            # next two cards 50 % chance to be common
            for i in range (4,6):
                rarity = random.uniform(0, 100)
                card_rarity = -1
                match rarity:
                    case x if x < 70:
                        card_rarity = 'C'
                    case x if x < 85:
                        card_rarity = 'R'
                    case x if x < 95:
                        card_rarity = 'RR'
                    case _:
                        card_rarity = 'RRR'
                pack_rarities.append(card_rarity)
            # at least one 'good' card in a pack
            rarity = random.uniform(0, 100)
            card_rarity = -1
            match rarity:
                case x if x < 50 :
                    card_rarity = 'R'
                case x if x < 87.5:
                    card_rarity = 'RR'
                case _:
                    card_rarity = 'RRR'
            pack_rarities.append(card_rarity)
            return pack_rarities
    @staticmethod
    def get_random_cards(rarities):
        selected_cards = []
        
        for rarity in rarities:
            all_cards = Cards.objects.filter(rarity= rarity, number__startswith="BT01")
            total_cards = all_cards.count()
            
            rindx = random.randint(0, total_cards - 1)
            card = all_cards[rindx]
            selected_cards.append(card)
        return selected_cards
    
    def get(self, request, username):
        
        # super_pack_rarity = random.uniform(0, 100)
        pack_rarities = PackOpenerView.choose_pack_rarities()
            # regular pack logic
        # get cards at end based on rarities
        cards = PackOpenerView.get_random_cards(pack_rarities)
        try:
            user_profile = UserProfile.objects.get(user__username = username)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)
            # this 404 wild lmao
        for card in cards:
            user_card, created = UserCard.objects.get_or_create(
                user_profile = user_profile,
                card = card
            )
            if not created:
                user_card.count +=1
            user_card.save()
        
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)


class AllCardsView(APIView):
    def get(self, request):
        cards = Cards.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
    
class UserProfileView(APIView):
    def get(self, request, username):
        user_profile = UserProfile.objects.get(user__username = username)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
class UserCardsView(APIView):
    def get(self, request, username):
        user_profile = UserProfile.objects.get(user__username = username)
        serializer = UserProfileSerializer(user_profile)
        return Response({"cards": serializer.data['cards']})
    
class LoginView(APIView):
    def post(self, request, username):
        password = request.data.get('password', None)
        
        if not password:
            return Response({"error": "Password is required"}, states = status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username = username, password = password)
        
        if user is not None:  # exists
            return Response({
                "success" : True,
                "message": "Login successful",
                "username": username
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Invalid login credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
            
class RegisterView(APIView):
    def post(self, request, username):
        password = request.data.get('password', None)
        if not password or not username:
            return Response({"error": "Username and password is required", "success": False}, states = status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username = username).exists():
            return Response({"error": "Username is taken", "success": False}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(username = username, password = password)
            user_profile = UserProfile.objects.create(user = user)
            return Response(
                {"message": "User successfully registered", "success": True}, status = status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                {"error": "server error", "success": False}, status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )