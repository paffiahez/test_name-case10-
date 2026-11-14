from django.shortcuts import render

def craft_events(request):
    return render(request, 'events_craft.html')