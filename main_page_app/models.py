from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    logo = models.URLField(default='https://place-hold.it/100x60', blank=True)
    description = models.TextField(blank=True)
    employee_count = models.IntegerField(default=0)

    def __str__(self):
        return f'компания - {self.name}; находится - {self.location}'

    class Meta:
        verbose_name = 'Компании'
        verbose_name_plural = verbose_name
        ordering = ['pk']


class Vacancy(models.Model):
    title = models.CharField(max_length=150)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    skills = models.TextField(blank=True)
    description = models.TextField(blank=True)
    salary_min = models.IntegerField(default=0, blank=True)
    salary_max = models.IntegerField(default=0, blank=True)
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        average_salary = (self.salary_min + self.salary_max) // 2
        return (
            f'id: {self.pk}; вакансия - {self.title}; '
            f'сред-зарплата - {average_salary}; '
            f'{self.company}.'
        )

    class Meta:
        verbose_name = 'Вакансии'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Specialty(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    picture = models.URLField(default='https://place-hold.it/100x60', blank=True)

    def __str__(self):
        return f'{self.pk} - {self.title}'

    class Meta:
        verbose_name = 'Специализации'
        verbose_name_plural = verbose_name
