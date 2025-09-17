from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('vacancies/',  views.vacancies_page, name='vacancies_page'),
    path('vacancies/cat/<str:group_of_vacancies>/', views.vacancies_specialty, name='vacancies_specialty'),
    path('vacancies/<int:vacancy_id>/', views.one_vacancy, name='one_vacancy'),
    path('companies/<int:companies_id>/', views.companies_page, name='companies_page'),
]
