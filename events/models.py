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
class EventRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'На рассмотрении'
        APPROVED = 'approved', 'Одобрена'
        REJECTED = 'rejected', 'Отклонена'

    title = models.CharField('Название мероприятия', max_length=200)
    event_type = models.CharField('Тип', max_length=20,
                                  choices=Event.EventType.choices)
    format = models.CharField('Формат', max_length=10,
                              choices=Event.Format.choices)
    date = models.DateField('Дата')
    duration = models.CharField('Длительность', max_length=50)
    organization = models.CharField('Организация', max_length=200)
    address = models.CharField('Адрес', max_length=300, blank=True, default='—')
    description = models.TextField('Описание')
    status = models.CharField('Статус', max_length=10,
                              choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField('Отправлена', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка на мероприятие'
        verbose_name_plural = 'Заявки на мероприятия'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.organization})'
