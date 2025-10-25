from django.apps import AppConfig


class UserCompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_company'
    verbose_name = 'Компании и вакансии пользователей'