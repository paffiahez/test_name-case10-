from collections import Counter
from .models import AnswerOption, StudyDirection

def calculate_result(answers):
    """answers: словарь {question_id: option_id} из формы."""
    scores = Counter()
    for option_id in answers.values():
        for s in AnswerOption.objects.filter(option_id=option_id).select_related('direction'):
            scores[s.direction] += s.weight
    # отсортированный список направлений от лучшего к худшему
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
