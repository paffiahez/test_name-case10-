"""
URL configuration for catalog_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalog.views import home
from events_jober.views import events_list
from events_craft.views import craft_events
from events_vuz.views import vuz_events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),           
    path('events/', events_list, name='events'), 
    path('craft/', craft_events, name='craft'),
    path('vuz/', vuz_events, name='vuz'),
]
