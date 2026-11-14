from django.shortcuts import render, redirect
from .db_handler import load_data, save_data
from datetime import datetime

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        data = load_data()
        users = data.get('users', {})
        
        if username in users and users[username]['password'] == password:
            request.session['user_id'] = username
            return redirect('profile')
        else:
            error = "Неверный логин или пароль."
            
    return render(request, 'pages/login.html', {'error': error})

def profile_view(request):
    username = request.session.get('user_id')
    if not username:
        return redirect('login')

    data = load_data()
    user_data = data['users'].get(username)

    if not user_data:
        return redirect('login')

    # Если это не студент, показываем заглушку
    if user_data.get('role') != 'student':
        return render(request, 'pages/not_student.html', {'user': user_data})

    # Если студент: обрабатываем сохранение анкеты
    if request.method == 'POST' and 'save_profile' in request.POST:
        data['users'][username]['profile'] = {
            'fio': request.POST.get('fio', ''),
            'phone': request.POST.get('phone', ''),
            'skills': request.POST.get('skills', ''),
            'experience': request.POST.get('experience', ''),
            'olympiads': request.POST.get('olympiads', ''),
        }
        save_data(data)
        return redirect('profile')

    # Ищем наставника
    mentor_info = None
    mentor_id = user_data.get('mentor_id')
    if mentor_id:
        mentor_info = data['users'].get(mentor_id)

    # Берем историю чата
    chat_messages = []
    if mentor_id:
        chat_key = f"{username}_{mentor_id}"
        chat_messages = data.get('chats', {}).get(chat_key, [])

    return render(request, 'pages/profile.html', {
        'username': username,
        'profile': user_data.get('profile', {}),
        'mentor': mentor_info,
        'chat_messages': chat_messages,
        'mentor_id': mentor_id
    })

def send_message(request):
    if request.method == 'POST':
        username = request.session.get('user_id')
        if not username:
            return redirect('login')

        message_text = request.POST.get('message', '').strip()
        mentor_id = request.POST.get('mentor_id')

        if message_text and mentor_id:
            data = load_data()
            chat_key = f"{username}_{mentor_id}"
            
            if 'chats' not in data:
                data['chats'] = {}
            if chat_key not in data['chats']:
                data['chats'][chat_key] = []

            current_time = datetime.now().strftime("%H:%M")
            data['chats'][chat_key].append({
                "sender": username,
                "text": message_text,
                "time": current_time
            })
            save_data(data)

        return redirect('profile')

def logout_view(request):
    request.session.flush()
    return redirect('home')

def home(request): return render(request, 'index.html')
def about(request): return render(request, 'pages/about.html')
def contacts(request): return render(request, 'pages/contacts.html')