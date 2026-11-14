from django.shortcuts import get_object_or_404, render

from .models import Event


def event_list(request):
    events = Event.objects.all()

    fmt = request.GET.get('format', 'all')
    typ = request.GET.get('type', 'all')
    org = request.GET.get('org', 'all')
    sort = request.GET.get('sort', 'asc')

    if fmt != 'all':
        events = events.filter(format=fmt)
    if typ != 'all':
        events = events.filter(event_type=typ)
    if org != 'all':
        events = events.filter(org_type=org)
    events = events.order_by('date' if sort == 'asc' else '-date')

    # запоминаем фильтры, чтобы ссылки на мероприятия их сохраняли
    params = request.GET.copy()
    params.pop('selected', None)
    querystring = params.urlencode()

    selected = None
    selected_id = request.GET.get('selected')
    if selected_id:
        selected = get_object_or_404(Event, pk=selected_id)

    return render(request, 'events/event_list.html', {
        'events': events,
        'selected': selected,
        'querystring': querystring,
        'filters': {'format': fmt, 'type': typ, 'org': org, 'sort': sort},
    })
