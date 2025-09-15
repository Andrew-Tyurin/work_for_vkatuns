from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacancies_page, name='vacancies_page'),
    path('<int:vacancies_id>/', views.one_vacancy, name='one_vacancy'),
    path('cat/<str:specialty_request>/', views.vacancies_specialty, name='vacancies_specialty'),
]
