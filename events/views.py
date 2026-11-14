from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Event, EventRequest
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def uni_events(request):
    context = _calendar_context(request)
    context['requests'] = EventRequest.objects.filter(
        status=EventRequest.Status.PENDING
    )
    return render(request, 'events/uni_events.html', context)


@staff_member_required
def handle_request(request, pk, action):
    req = get_object_or_404(EventRequest, pk=pk)

    if request.method == 'POST':
        if action == 'accept':
            Event.objects.create(
                title=req.title,
                event_type=req.event_type,
                format=req.format,
                date=req.date,
                duration=req.duration,
                organizer=req.organization,
                org_type=Event.OrgType.EMPLOYER,
                address=req.address,
                description=req.description,
            )
            req.status = EventRequest.Status.APPROVED
        elif action == 'reject':
            req.status = EventRequest.Status.REJECTED
        req.save()

    return redirect('uni_events')


def _calendar_context(request):
    """Общая сборка данных для обеих страниц календаря."""
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

    params = request.GET.copy()
    querystring = params.urlencode()

    selected = None
    selected_id = request.GET.get('selected')
    if selected_id:
        selected = get_object_or_404(Event, pk=selected_id)

    return {
        'events': events,
        'selected': selected,
        'querystring': querystring,
        'filters': {'format': fmt, 'type': typ, 'org': org, 'sort': sort},
    }


def event_list(request):
    return render(request, 'events/event_list.html', _calendar_context(request))


def employer_events(request):
    return render(request, 'events/employer_events.html', _calendar_context(request))


def event_request(request):
    if request.method == 'POST':
        EventRequest.objects.create(
            title=request.POST.get('title', ''),
            event_type=request.POST.get('event_type', ''),
            format=request.POST.get('format', ''),
            date=request.POST.get('date') or timezone.now().date(),
            duration=request.POST.get('duration', ''),
            organization=request.POST.get('organization', ''),
            address=request.POST.get('address') or '—',
            description=request.POST.get('description', ''),
        )
        return redirect('/events/employer/?sent=1')
    return redirect('employer_events')
