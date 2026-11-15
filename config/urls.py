from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from main.views import about, contacts
from catalog.views import login_view, logout_view, dashboard_view, profile_view, send_message, employer_events_view, employer_students_view, employer_documents_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Корень сайта - это ВСЕГДА страница входа (логин)
    path('', login_view, name='login'),
    
    # Дублирующий маршрут для /login/ (чтобы не было 404)
    path('login/', login_view, name='login_page'),
    
    # Главная страница с кнопками (доступна только после входа)
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Профиль и чат
    path('profile/', profile_view, name='profile'),
    path('send_message/', send_message, name='send_message'),
    
    # Статические страницы
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    
    # Приложения
    path('abitur/', include('abitur_page.urls')),
    path('proftests/', include('proftests.urls')),
    path('events/', include('events.urls')),
    
    # Выход
    path('logout/', logout_view, name='logout'),

    path('employer/events/', employer_events_view, name='employer_events'),
    path('employer/students/', employer_students_view, name='employer_students'),
    path('employer/documents/', employer_documents_view, name='employer_documents'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()