from django.shortcuts import render
from .models import Offer

def offer_list(request):
    offers = Offer.objects.filter(is_active=True)
    return render(request, "abitur_page/target_study.html", {"offers": offers})

def target_study(request):
    # This view currently does the same as offer_list to prevent errors
    offers = Offer.objects.filter(is_active=True)
    return render(request, "abitur_page/target_study.html", {"offers": offers})

