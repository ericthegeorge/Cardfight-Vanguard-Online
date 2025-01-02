from django.urls import path
from .views import PackOpenerView

urlpatterns = [
    path('open-pack/', PackOpenerView.as_view()),
]