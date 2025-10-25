from django.urls import path
from . import views


urlpatterns = [
    path('', views.my_company, name='my_company'),
    path('letsstart/', views.my_company_start, name='my_company_start'),
    path('create/', views.my_company_create, name='my_company_create'),
    path('vacancies/', views.my_company_vacancies_list, name='my_company_vacancies_list'),
    path('vacancies/create/', views.create_vacancy_my_company, name='create_vacancy_my_company'),
    path('vacancies/<int:vacancy_id>/', views.my_company_vacancy, name='my_company_vacancy'),
]