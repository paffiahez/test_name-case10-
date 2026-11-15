from django.shortcuts import render, redirect
from .db_handler import load_data, save_data
from datetime import datetime

# --- ЛОГИН / ВЫХОД ---
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        data = load_data()
        users = data.get('users', {})
        
        if username in users and users[username]['password'] == password:
            request.session['user_id'] = username
            return redirect('dashboard')
        else:
            error = "Неверный логин или пароль."
            
    return render(request, 'pages/login.html', {'error': error})

def logout_view(request):
    request.session.flush()
    return redirect('/')

# --- РОУТЕР (Главная страница после входа) ---
def dashboard_view(request):
    username = request.session.get('user_id')
    if not username:
        return redirect('login')
    
    data = load_data()
    user = data['users'].get(username)
    if not user:
        return redirect('login')
        
    role = user.get('role')

    # 1. СТУДЕНТ
    if role == 'student':
        return render(request, 'main/index.html', {'user': user}) 
        
    # 2. СОТРУДНИК ВУЗА (Ведем на новую главную с 3 кнопками)
    elif role == 'staff':
        return render(request, 'pages/staff_dashboard.html', {'user': user})
        
    # 3. РАБОТОДАТЕЛЬ ИЛИ НАСТАВНИК
    elif role == 'employer' or role == 'mentor':
        return render(request, 'pages/employer_dashboard.html', {'user': user})
        
    # 4. ОСТАЛЬНЫЕ
    else:
        return render(request, 'pages/not_student.html', {'user': user})

# --- ПРОФИЛЬ ---
def profile_view(request):
    username = request.session.get('user_id')
    if not username:
        return redirect('login')

    data = load_data()
    user_data = data['users'].get(username)
    if not user_data:
        return redirect('login')

    role = user_data.get('role')

    if role == 'student':
        if request.method == 'POST' and 'save_profile' in request.POST:
            data['users'][username]['profile'] = {
                'fio': request.POST.get('fio', ''), 'phone': request.POST.get('phone', ''),
                'skills': request.POST.get('skills', ''), 'experience': request.POST.get('experience', ''),
                'olympiads': request.POST.get('olympiads', ''),
            }
            save_data(data)
            return redirect('profile')

        mentor_info = data['users'].get(user_data.get('mentor_id')) if user_data.get('mentor_id') else None
        chat_messages = data.get('chats', {}).get(f"{username}_{user_data.get('mentor_id')}", []) if user_data.get('mentor_id') else []

        return render(request, 'pages/profile.html', {
            'username': username, 'profile': user_data.get('profile', {}),
            'mentor': mentor_info, 'chat_messages': chat_messages, 'mentor_id': user_data.get('mentor_id')
        })
    else:
        return render(request, 'pages/not_student.html', {'user': user_data})

# --- ОТПРАВКА СООБЩЕНИЯ В ЧАТ ---
def send_message(request):
    if request.method == 'POST':
        username = request.session.get('user_id')
        if not username: return redirect('login')

        message_text = request.POST.get('message', '').strip()
        mentor_id = request.POST.get('mentor_id')

        if message_text and mentor_id:
            data = load_data()
            chat_key = f"{username}_{mentor_id}"
            if 'chats' not in data: data['chats'] = {}
            if chat_key not in data['chats']: data['chats'][chat_key] = []

            data['chats'][chat_key].append({
                "sender": username, "text": message_text, "time": datetime.now().strftime("%H:%M")
            })
            save_data(data)
        return redirect('profile')

# --- СТРАНИЦЫ РАБОТОДАТЕЛЯ ---
def employer_events_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    
    data = load_data()
    user = data['users'].get(username)
    events = data.get('events', [])
    
    if request.method == 'POST' and 'create_request' in request.POST:
        new_req = {
            "id": int(datetime.now().timestamp()),
            "dateSubmitted": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "status": "pending",
            "eventData": {
                "title": request.POST.get('title'), "date": request.POST.get('date'),
                "format": request.POST.get('format'), "type": request.POST.get('type'),
                "time": request.POST.get('time'), "org": request.POST.get('org'),
                "orgType": "employer", "address": request.POST.get('address'), "desc": request.POST.get('desc')
            }
        }
        data.setdefault('requests', []).append(new_req)
        save_data(data)
        return redirect('employer_events')

    return render(request, 'pages/events_jober.html', {'user': user, 'events': events})

def employer_students_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    
    data = load_data()
    students = []
    for uname, u in data['users'].items():
        if u.get('role') == 'student':
            profile = u.get('profile', {})
            tag = u.get('tag', 'Абитуриент')
            students.append({
                'username': uname,
                'name': u.get('name'),
                'profile': profile,
                'tag': tag,
                'pdf_url': f"/static/grades/{uname}_grades.pdf"
            })
            
    return render(request, 'pages/employer_students.html', {'students': students})

def employer_documents_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    return render(request, 'pages/employer_documents.html')

# --- НОВЫЕ СТРАНИЦЫ СОТРУДНИКА ВУЗА ---

def staff_events_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    
    data = load_data()
    user = data['users'].get(username)
    events = data.get('events', [])
    requests = data.get('requests', [])
    
    # Обработка одобрения заявки
    if request.method == 'POST' and 'accept_request' in request.POST:
        req_id = int(request.POST.get('request_id'))
        req = next((r for r in requests if r['id'] == req_id), None)
        if req:
            req['status'] = 'accepted'
            new_event = req['eventData']
            new_event['id'] = int(datetime.now().timestamp())
            events.append(new_event)
            save_data(data)
        return redirect('staff_events')

    # Отдаем страницу Насти для сотрудника (с заявками)
    return render(request, 'pages/events_vuz.html', {'user': user, 'events': events, 'requests': [r for r in requests if r['status'] == 'pending']})

def staff_students_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    
    data = load_data()
    students = []
    for uname, u in data['users'].items():
        if u.get('role') == 'student':
            profile = u.get('profile', {})
            tag = u.get('tag', 'Абитуриент')
            company = u.get('company', '') # Если статус "Работает"
            students.append({
                'username': uname,
                'name': u.get('name'),
                'profile': profile,
                'tag': tag,
                'company': company
            })
            
    return render(request, 'pages/staff_students.html', {'students': students})

def staff_stats_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    return render(request, 'pages/staff_stats.html')

def staff_events_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    return render(request, 'pages/events_vuz.html', {'user': username})

def companies_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    return render(request, 'pages/companies.html')

def contracts_view(request):
    username = request.session.get('user_id')
    if not username: return redirect('login')
    return render(request, 'pages/contracts.html')