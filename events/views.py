from django.shortcuts import render, redirect
from catalog.db_handler import load_data
import json

def events_list(request):
    # Вместо несуществующего events_jober.html отдаем нашу страницу для студентов
    # (или можно создать events_jober.html и положить его в events/templates/)
    username = request.session.get('user_id')
    if not username:
        return redirect('login')
    
    data = load_data()
    events = data.get('events', [])
    
    return render(request, 'pages/events_student.html', {
        'username': username, 
        'events_json': json.dumps(events)
    })

def student_events(request):
    username = request.session.get('user_id')
    if not username:
        return redirect('login')
    
    data = load_data()
    events = data.get('events', [])
    
    # Передаем данные в шаблон в формате JSON, чтобы JS Насти мог их прочитать
    return render(request, 'pages/events_student.html', {
        'username': username, 
        'events_json': json.dumps(events)
    })