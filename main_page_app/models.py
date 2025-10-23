from django.db import models
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    location = models.CharField(max_length=50, verbose_name='город')
    logo = models.ImageField(upload_to='companies', default='https://place-hold.it/100x60', blank=True, verbose_name='логотип')
    description = models.TextField(blank=True, verbose_name='инф. о компании')
    employee_count = models.IntegerField(default=0, verbose_name='кол-во сотрудников')

    def __str__(self):
        return f'компания - {self.name}; находится - {self.location}'

    def get_absolute_url(self):
        return reverse('vacancies_by_companies', kwargs={'company_id': self.id}) # или args=(self.id,)

    class Meta:
        verbose_name = 'Компанию'
        verbose_name_plural = 'Компании'
        ordering = ['pk']


class Specialty(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name='код')
    title = models.CharField(max_length=30, verbose_name='title')
    picture = models.ImageField(upload_to='specialties', default='https://place-hold.it/100x60', blank=True, verbose_name='картинка')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacancies_by_specialty', args=(self.code,))  # или kwargs={'specialty_slug': self.code}

    class Meta:
        verbose_name = 'Специализацию'
        verbose_name_plural = 'Специализации'


class Vacancy(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.CASCADE,
        to_field="code",
        related_name="vacancies",
        verbose_name='Специализация'
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="vacancies",
        verbose_name='Компания',
    )
    skills = models.TextField(blank=True, verbose_name='Навыки')
    description = models.TextField(blank=True, verbose_name='Текст')
    salary_min = models.IntegerField(default=0, blank=True, verbose_name='Зарплата от')
    salary_max = models.IntegerField(default=0, blank=True, verbose_name='Зарплата до')
    published_at = models.DateField(auto_now_add=True, verbose_name='Опубликовано')

    def __str__(self):
        average_salary = (self.salary_min + self.salary_max) // 2
        return (
            f'id: {self.pk}; вакансия - {self.title}; '
            f'сред-зарплата - {average_salary}; '
            f'{self.company}.'
        )

    def get_absolute_url(self):
        return reverse('one_vacancy', args=(self.id,))

    class Meta:
        verbose_name = 'Вакансию'
        verbose_name_plural = 'Вакансии'
        ordering = ['id']
