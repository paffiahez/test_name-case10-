from django.db import models


class Program(models.Model):
    code = models.CharField('Код направления', max_length=10, unique=True)
    title = models.CharField('Название', max_length=255)
    form = models.CharField('Форма обучения', max_length=50)
    places = models.PositiveIntegerField('Целевые места')
    duration = models.CharField('Срок обучения', max_length=20)
    avg_score = models.CharField('Средний балл', max_length=30)
    price = models.CharField('Стоимость', max_length=50)
    pdf = models.CharField('Файл расписания', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Направление целевого обучения'
        verbose_name_plural = 'Направления целевого обучения'
        ordering = ['code']

    def __str__(self):
        return f'{self.code} {self.title}'


class ProgramNote(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE,
                                related_name='notes', verbose_name='Направление')
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    label = models.CharField('Метка', max_length=100)   # «Шанс поступить», «Совет»…
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'Заметка «Полезно знать»'
        verbose_name_plural = 'Заметки «Полезно знать»'
        ordering = ['order']

    def __str__(self):
        return f'{self.program.code}: {self.label}'
