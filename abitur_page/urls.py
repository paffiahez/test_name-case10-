from django.urls import path
from . import views

urlpatterns = [
    path('offer_list/', views.offer_list, name='offer_list'),
    path('target_study/', views.target_study, name='target_study'),
]
