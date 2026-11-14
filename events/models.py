from django.db import models


class Event(models.Model):
    class OrgType(models.TextChoices):
        UNIVERSITY = 'uni', 'От вуза'
        EMPLOYER = 'employer', 'От работодателей'

    class Format(models.TextChoices):
        OFFLINE = 'Офлайн', 'Офлайн'
        ONLINE = 'Онлайн', 'Онлайн'

    class EventType(models.TextChoices):
        LECTURE = 'Лекция', 'Лекция'
        EXCURSION = 'Экскурсия', 'Экскурсия'
        OLYMPIAD = 'Олимпиада', 'Олимпиада'
        WORKSHOP = 'Мастер-класс', 'Мастер-класс'

    title = models.CharField('Название', max_length=200)
    event_type = models.CharField('Тип', max_length=20, choices=EventType.choices)
    format = models.CharField('Формат', max_length=10, choices=Format.choices)
    date = models.DateField('Дата проведения')
    duration = models.CharField('Длительность', max_length=50, default='1 ч. 00 мин.')
    organizer = models.CharField('Организатор', max_length=200)
    org_type = models.CharField('Тип организатора', max_length=10,
                                choices=OrgType.choices, default=OrgType.UNIVERSITY)
    address = models.CharField('Адрес', max_length=300, blank=True, default='—')
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['date']

    def __str__(self):
        return self.title
