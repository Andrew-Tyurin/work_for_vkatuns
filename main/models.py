from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    location = models.CharField(max_length=50, verbose_name='Город')
    logo = models.ImageField(
        upload_to='companies',
        default='https://place-hold.it/100x60', blank=True,
        verbose_name='Логотип',
    )
    description = models.TextField(blank=True, verbose_name='Инф. о компании')
    employee_count = models.IntegerField(default=0, verbose_name='Кол-во сотрудников')
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='owner',
    )

    def __str__(self):
        return f'Компания - {self.name}; Находится - {self.location}'

    class Meta:
        verbose_name = 'Компанию'
        verbose_name_plural = 'Компании'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('vacancies_by_companies', kwargs={'company_id': self.id})


class Specialty(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name='Код')
    title = models.CharField(max_length=30, verbose_name='Направление')
    picture = models.ImageField(
        upload_to='specialties',
        default='https://place-hold.it/100x60',
        blank=True,
        verbose_name='Картинка',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специализацию'
        verbose_name_plural = 'Специализации'

    def get_absolute_url(self):
        return reverse('vacancies_by_specialty', args=(self.code,))  # или kwargs={'specialty_slug': self.code}


class Vacancy(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.CASCADE,
        to_field="code",
        related_name="vacancies",
        verbose_name='Специализация',
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name='Компания',
    )
    skills = models.TextField(blank=True, verbose_name='Навыки')
    description = models.TextField(blank=True, verbose_name='Текст')
    salary_min = models.IntegerField(default=0, blank=True, verbose_name='Зарплата от')
    salary_max = models.IntegerField(default=0, blank=True, verbose_name='Зарплата до')
    published_at = models.DateField(auto_now_add=True, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.company}; Вакансия - {self.title};'

    class Meta:
        verbose_name = 'Вакансию'
        verbose_name_plural = 'Вакансии'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('one_vacancy', args=(self.id,))


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


class Resume(models.Model):
    class Status(models.TextChoices):
        MAX_ACTIVE = 'max_active', 'Ищу работу'
        ACTIVE = 'active', 'Рассматриваю предложения'
        NON_ACTIVE = 'non_active', 'Не ищу работу'

    class Grade(models.TextChoices):
        INTERN = 'intern', 'Стажер'
        JUNIOR = 'Junior', 'Джуниор'
        MIDDLE = 'middle', 'Миддл'
        SENIOR = 'senior', 'Синьор'
        LID = 'lid', 'Лид'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='my_resume',
        verbose_name='Резюме',
    )
    name = models.CharField(max_length=80, verbose_name='Имя')
    surname = models.CharField(max_length=80, verbose_name='Фамилия')
    status = models.CharField(
        max_length=26,
        choices = Status.choices,
        default=Status.MAX_ACTIVE,
        verbose_name='Готовность к работе',
    )
    salary = models.IntegerField(default=1, verbose_name='Вознаграждение')
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        to_field="code",
        related_name="resume",
        verbose_name='Специализация',
    )
    grade = models.CharField(
        max_length=20,
        choices=Grade.choices,
        default=Grade.MIDDLE,
        verbose_name='Квалификация',
    )
    education = models.TextField(
        blank=True,
        default='4 класса начальной школы.',
        verbose_name='Образование',
    )
    experience = models.TextField(
        blank=True,
        default='Яндекс...  доставка',
        verbose_name='Опыт работы',
    )
    portfolio = models.URLField(
        blank=True,
        max_length=120,
        verbose_name = 'Портфолио',
    )


    def __str__(self):
        return f'{self.user}, {self.grade}, {self.status}'

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = verbose_name
