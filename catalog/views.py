from django.shortcuts import render

from .models import Program


def program_list(request):
    programs = Program.objects.prefetch_related('notes')
    selected = None
    selected_id = request.GET.get('selected')
    if selected_id:
        selected = programs.filter(pk=selected_id).first()
    return render(request, 'catalog/program_list.html', {
        'programs': programs,
        'selected': selected,
    })
