from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('student/', views.student_events, name='student_events'),
]