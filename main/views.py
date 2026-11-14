from django.shortcuts import render

def main(request):
    return render(request, 'main/index.html')

def about(request):
    # Указываем путь к папке pages внутри catalog
    return render(request, 'main/about.html')

def contacts(request):
    # Указываем путь к папке pages внутри catalog
    return render(request, 'main/contacts.html')