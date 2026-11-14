from django.db import models


class StudyDirection(models.Model):
    """Направление подготовки (например, «Информационные технологии»)."""
    name = models.CharField('Название', max_length=200)
    code = models.SlugField('Код', unique=True, help_text='Латиницей, например "it", "medicine"')
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Направление обучения'
        verbose_name_plural = 'Направления обучения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Test(models.Model):
    """Профориентационный тест."""
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title


class Question(models.Model):
    """Вопрос теста."""
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест',
    )
    text = models.TextField('Текст вопроса')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class AnswerOption(models.Model):
    """Вариант ответа на вопрос."""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Вопрос',
    )
    text = models.CharField('Текст варианта', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class AnswerOptionScore(models.Model):
    """Сколько баллов вариант ответа даёт каждому направлению."""
    option = models.ForeignKey(
        AnswerOption,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='Вариант ответа',
    )
    direction = models.ForeignKey(
        StudyDirection,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='Направление',
    )
    weight = models.PositiveIntegerField(
        'Баллы', default=1,
        help_text='Сколько баллов получит направление при выборе этого варианта',
    )

    class Meta:
        verbose_name = 'Связка «вариант — направление»'
        verbose_name_plural = 'Баллы вариантов ответов'
        unique_together = ('option', 'direction')

    def __str__(self):
        return f'{self.option} → {self.direction}: {self.weight}'
