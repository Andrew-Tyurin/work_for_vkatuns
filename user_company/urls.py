from django.urls import path
from . import views


urlpatterns = [
    path('', views.MyCompanyView.as_view(), name='my_company'),
    path('letsstart/', views.MyCompanyStartView.as_view(), name='my_company_start'),
    path('create/', views.CreateMyCompanyView.as_view(), name='my_company_create'),
    path('vacancies/', views.MyCompanyVacanciesListView.as_view(), name='my_company_vacancies_list'),
    path('vacancies/create/', views.create_vacancy_my_company, name='create_vacancy_my_company'),
    path('vacancies/<int:vacancy_id>/', views.MyCompanyVacancyView.as_view(), name='my_company_vacancy'),
]
