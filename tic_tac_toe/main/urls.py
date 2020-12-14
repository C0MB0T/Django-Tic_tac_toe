from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new/', views.new),
    path('game/<str:code>', views.game),
    path('join/<str:code>', views.join),
]