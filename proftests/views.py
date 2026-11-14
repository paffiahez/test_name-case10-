from collections import Counter
from .models import AnswerOption, StudyDirection
from collections import Counter
from django.shortcuts import get_object_or_404, render
from .models import AnswerOption, Test


def test_list(request):
    tests = Test.objects.filter(is_active=True)
    return render(request, 'abitur_page/test_list.html', {'tests': tests})


def test_detail(request, slug):
    test = get_object_or_404(Test, slug=slug, is_active=True)
    questions = test.questions.prefetch_related('options')

    result = None
    if request.method == 'POST':
        # собираем выбранные варианты по каждому вопросу
        option_ids = []
        for question in questions:
            value = request.POST.get(f'q{question.id}')
            if value:
                option_ids.append(value)

        options = (AnswerOption.objects.filter(pk__in=option_ids)
                   .prefetch_related('scores__direction'))

        scores = Counter()
        for option in options:
            for s in option.scores.all():
                scores[s.direction] += s.weight

        max_score = max(scores.values(), default=0)
        top = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0].name))[:5]
        result = [
            {
                'direction': direction,
                'score': score,
                'percent': round(score / max_score * 100) if max_score else 0,
            }
            for direction, score in top
        ]

    return render(request, 'abitur_page/test_detail.html', {
        'test': test,
        'questions': questions,
        'result': result,
    })

def calculate_result(answers):
    """answers: словарь {question_id: option_id} из формы."""
    scores = Counter()
    for option_id in answers.values():
        for s in AnswerOption.objects.filter(option_id=option_id).select_related('direction'):
            scores[s.direction] += s.weight
    # отсортированный список направлений от лучшего к худшему
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
