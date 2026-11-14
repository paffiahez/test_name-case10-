from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'pages/about.html') 

def contacts(request):
    return render(request, 'pages/contacts.html')

def login(request):
    return render(request, 'pages/login.html')