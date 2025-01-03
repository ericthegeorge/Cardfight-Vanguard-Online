from django.urls import path
from .views import PackOpenerView
from .views import AllCardsView


urlpatterns = [
    path('open-pack/', PackOpenerView.as_view(), name='open_pack'),
    path('all-cards/', AllCardsView.as_view(), name='all_cards'),
]