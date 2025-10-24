from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('vacancies/',  views.AllVacanciesView.as_view(), name='vacancies_page'),
    path('vacancies/cat/<str:specialty_slug>/', views.VacanciesBySpecialtyView.as_view(), name='vacancies_by_specialty'),
    path('vacancies/company/<int:company_id>/', views.VacanciesByCompaniesView.as_view(), name='vacancies_by_companies'),
    path('vacancies/<int:vacancy_id>/', views.OneVacancyView.as_view(), name='one_vacancy'),
    path('vacancies/<int:vacancy_id>/send/', views.send_application, name='send_application'),

    path('mycompany/', views.my_company, name='my_company'),
    path('mycompany/letsstart/', views.my_company_start, name='my_company_start'),
    path('mycompany/create/', views.my_company_create, name='my_company_create'),
    path('mycompany/vacancies/', views.my_company_vacancies_list, name='my_company_vacancies_list'),
    path('mycompany/vacancies/create/', views.create_vacancy_my_company, name='create_vacancy_my_company'),
    path('mycompany/vacancies/<int:vacancy_id>/', views.my_company_vacancy, name='my_company_vacancy'),
]
