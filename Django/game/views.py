from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Cards, UserProfile
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
                    case x if x < 88:
                        card_rarity = 'R'
                    case x if x < 97:
                        card_rarity = 'RR'
                    case _:
                        card_rarity = 'RRR'
                pack_rarities.append(card_rarity)
            # at least one 'good' card in a pack
            rarity = random.uniform(0, 100)
            card_rarity = -1
            match rarity:
                case x if x < 40 :
                    card_rarity = 'R'
                case x if x < 85:
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
        
        super_pack_rarity = random.uniform(0, 100)
        pack_rarities = PackOpenerView.choose_pack_rarities()
            # regular pack logic
        # get cards at end based on rarities
        cards = PackOpenerView.get_random_cards(pack_rarities)
        serializer = CardSerializer(cards, many=True)
        user_profile = UserProfile.objects.get(user__username = username)
        user_profile.cards.add(*cards)
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