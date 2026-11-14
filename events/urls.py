from django.urls import path

from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('employer/', views.employer_events, name='employer_events'),
    path('uni/', views.uni_events, name='uni_events'),
    path('request/<int:pk>/<str:action>/', views.handle_request, name='handle_request'),
    path('request/', views.event_request, name='event_request'),
]
