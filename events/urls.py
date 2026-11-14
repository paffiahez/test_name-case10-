from django.urls import path

from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('request/', views.event_request, name='event_request'),

]
