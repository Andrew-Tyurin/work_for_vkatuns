from django.urls import path
from main import views
from main.accounts import views as accounts_views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('vacancies/', views.AllVacanciesView.as_view(), name='vacancies_page'),
    path('vacancies/cat/<str:specialty_slug>/', views.VacanciesBySpecialtyView.as_view(), name='vacancies_by_specialty'),
    path('vacancies/company/<int:company_id>/', views.VacanciesByCompaniesView.as_view(), name='vacancies_by_companies'),
    path('vacancies/<int:vacancy_id>/', views.OneVacancyView.as_view(), name='one_vacancy'),
    path('vacancies/<int:vacancy_id>/send/', views.send_application, name='send_application'),
    path('search/', views.SearchVacanciesView.as_view(), name='search_vacancy'),

    path('mycompany/', views.MyCompanyView.as_view(), name='my_company'),
    path('mycompany/letsstart/', views.MyCompanyStartView.as_view(), name='my_company_start'),
    path('mycompany/create/', views.CreateMyCompanyView.as_view(), name='my_company_create'),
    path('mycompany/vacancies/', views.MyCompanyVacanciesListView.as_view(), name='my_company_vacancies_list'),
    path('mycompany/vacancies/create/', views.CreateMyCompanyVacancyView.as_view(), name='create_vacancy_my_company'),
    path('mycompany/vacancies/<int:vacancy_id>/', views.MyCompanyVacancyView.as_view(), name='my_company_vacancy'),

    path('login/', accounts_views.LoginUserView.as_view(), name='login'),
    path('register/', accounts_views.RegisterUserView.as_view(), name='register'),
    path('logout/', accounts_views.LogoutUserView.as_view(), name='logout'),

    path('myresume/', views.MyResumeView.as_view(), name='my_resume'),
    path('myresume/letsstart/', views.MyResumeStartView.as_view(), name='my_resume_start'),
    path('myresume/create/', views.CreateMyResumeView.as_view(), name='my_resume_create'),
    path('resume/', views.AllResumeView.as_view(), name='all_resume'),

]
