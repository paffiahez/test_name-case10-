from django.shortcuts import render

def vuz_events(request):
    return render(request, 'events_vuz.html')