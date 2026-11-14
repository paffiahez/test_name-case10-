from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Event, EventRequest


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


def event_request(request):
    if request.method == 'POST':
        org_type_default = Event.OrgType.EMPLOYER
        req = EventRequest.objects.create(
            title=request.POST.get('title', ''),
            event_type=request.POST.get('event_type', ''),
            format=request.POST.get('format', ''),
            date=request.POST.get('date') or timezone.now().date(),
            duration=request.POST.get('duration', ''),
            organization=request.POST.get('organization', ''),
            address=request.POST.get('address') or '—',
            description=request.POST.get('description', ''),
        )
        return redirect(f'/events/?sent=1#{req.pk}')
    return redirect('event_list')
