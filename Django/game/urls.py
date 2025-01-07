from django.urls import path
from .views import PackOpenerView
from .views import AllCardsView, UserProfileView, LoginView, RegisterView, UserCardsView


urlpatterns = [
    # path('open-pack/', PackOpenerView.as_view(), name='open_pack'),
    path('user/<str:username>/all-cards/', AllCardsView.as_view(), name='all_cards'),
    path('user/<str:username>/', UserProfileView.as_view, name = "user_profile"),
    path('user/<str:username>/open-pack/', PackOpenerView.as_view(), name='open_pack'),
    path('user/<str:username>/login/', LoginView.as_view(), name='user_login'),
    path('user/<str:username>/register/', RegisterView.as_view(), name = 'user_register'),
    path('user/<str:username>/user-cards/', UserCardsView.as_view(), name = 'user_cards'),
]