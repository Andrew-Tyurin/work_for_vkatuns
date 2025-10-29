from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from user_company.models import Vacancy


class Application(models.Model):
    written_username = models.CharField(max_length=80, verbose_name='Имя')
    written_phone = PhoneNumberField(region='RU', verbose_name='Телефон')
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(
        Vacancy,
        related_name='applications',
        verbose_name='Вакансия',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='applications',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    def __str__(self):
        return f'{self.user}; откликнулся на: {self.vacancy.title}; компании - {self.vacancy.company.name}'

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
