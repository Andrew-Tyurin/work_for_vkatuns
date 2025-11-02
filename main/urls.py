from django.urls import path

from main.accounts import views as accounts_views
from main.views import main as main_views
from main.views import mycompany as mycompany_views
from main.views import myresume as myresume_views

urlpatterns = [
    path('', main_views.MainPageView.as_view(), name='main_page'),
    path('vacancies/', main_views.AllVacanciesView.as_view(), name='vacancies_page'),
    path('vacancies/cat/<str:specialty_slug>/', main_views.VacanciesBySpecialtyView.as_view(), name='vacancies_by_specialty'),
    path('vacancies/company/<int:company_id>/', main_views.VacanciesByCompaniesView.as_view(), name='vacancies_by_companies'),
    path('vacancies/<int:vacancy_id>/', main_views.OneVacancyView.as_view(), name='one_vacancy'),
    path('vacancies/<int:vacancy_id>/send/', main_views.send_application, name='send_application'),
    path('search/', main_views.SearchVacanciesView.as_view(), name='search_vacancy'),

    path('mycompany/', mycompany_views.MyCompanyView.as_view(), name='my_company'),
    path('mycompany/letsstart/', mycompany_views.MyCompanyStartView.as_view(), name='my_company_start'),
    path('mycompany/create/', mycompany_views.CreateMyCompanyView.as_view(), name='my_company_create'),
    path('mycompany/vacancies/', mycompany_views.MyCompanyVacanciesListView.as_view(), name='my_company_vacancies_list'),
    path('mycompany/vacancies/create/', mycompany_views.CreateMyCompanyVacancyView.as_view(), name='create_vacancy_my_company'),
    path('mycompany/vacancies/<int:vacancy_id>/', mycompany_views.MyCompanyVacancyView.as_view(), name='my_company_vacancy'),

    path('login/', accounts_views.LoginUserView.as_view(), name='login'),
    path('register/', accounts_views.RegisterUserView.as_view(), name='register'),
    path('logout/', accounts_views.LogoutUserView.as_view(), name='logout'),

    path('myresume/', myresume_views.MyResumeView.as_view(), name='my_resume'),
    path('myresume/letsstart/', myresume_views.MyResumeStartView.as_view(), name='my_resume_start'),
    path('myresume/create/', myresume_views.CreateMyResumeView.as_view(), name='my_resume_create'),
    path('resume/', myresume_views.AllResumeView.as_view(), name='all_resume'),

]
