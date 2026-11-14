from django.db import models
from django.utils.text import slugify


class Offer(models.Model):
    offer_id = models.AutoField("ID предложения", primary_key=True)
    code = models.CharField("Код направления", max_length=20, db_index=True)
    title = models.CharField("Название направления", max_length=255)
    name = models.CharField("Название программы вуза", max_length=255)
    employer = models.CharField("Предприятие (работодатель)", max_length=255)
    employer_address = models.CharField("Адрес предприятия", max_length=255, blank=True)
    start_date = models.DateField("Начало приёма заявок", null=True, blank=True)
    end_date = models.DateField("Окончание приёма заявок", null=True, blank=True)
    total_places = models.PositiveSmallIntegerField("Количество целевых мест", default=0)
    is_active = models.BooleanField("Активно", default=True)
    total_applications = models.PositiveSmallIntegerField("Количество поданных заявок", default=0)
    slug = models.SlugField("URL-идентификатор", unique=True, blank=True)

    class Meta:
        ordering = ['-is_active', 'code']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.code}-{self.employer}", allow_unicode=True)[:50]
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.code} {self.title} — {self.employer}"