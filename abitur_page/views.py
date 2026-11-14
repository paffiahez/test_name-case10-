from django.shortcuts import render
from .models import Offer

def offer_list(request):
    offers = Offer.objects.filter(is_active=True)
    #offers = Offer.objects.all() 
    return render(request, "target_study.html", {"offers": offers})
