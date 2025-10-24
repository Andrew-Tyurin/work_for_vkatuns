from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
# from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from .models import Specialty, Company, Vacancy


class MainPageView(TemplateView):
    template_name = 'main_page_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty_list'] = Specialty.objects.annotate(count=Count('vacancies'))
        context['company_list'] = Company.objects.annotate(count=Count('vacancies'))
        return context


class AllVacanciesView(ListView):
    model = Vacancy
    template_name = 'main_page_app/vacancies.html'

    def get_queryset(self):
        return super().get_queryset().select_related('company')


class VacanciesBySpecialtyView(AllVacanciesView, ListView):
    allow_empty = True

    def get_queryset(self):
        specialty = self.kwargs['specialty_slug']
        return Vacancy.objects.filter(specialty=specialty).select_related('company')

    def get_context_data(self, **kwargs):
        specialty = get_object_or_404(Specialty, code=self.kwargs['specialty_slug'])
        return super().get_context_data(specialty_ru=specialty.title, **kwargs)


class VacanciesByCompaniesView(AllVacanciesView, ListView):
    allow_empty = True

    def get_queryset(self):
        company = self.kwargs['company_id']
        return Vacancy.objects.filter(company=company).select_related('company')

    def get_context_data(self, **kwargs):
        company = get_object_or_404(Company, id=self.kwargs['company_id'])
        return super().get_context_data(company=company, **kwargs)


class OneVacancyView(DetailView):
    template_name = 'main_page_app/card_one_vacancy.html'
    model = Vacancy
    pk_url_kwarg = 'vacancy_id'


def my_company_start(request):
    return render(request, 'main_page_app/user/mycompany_start.html', {})

def my_company_create(request):
    return render(request, 'main_page_app/user/mycompany_create.html', {})


def my_company(request):
    return render(request, 'main_page_app/user/mycompany.html', {})


def my_company_vacancies_list(request):
    return render(request, 'main_page_app/user/mycompany_vacancies_list.html', {})


def create_vacancy_my_company(request):
    return render(request, 'main_page_app/user/mycompany_vacancy_create.html', {})

def my_company_vacancy(request, vacancy_id):
    return render(request, 'main_page_app/user/mycompany_vacancy.html', {})





def send_application(request, vacancy_id):
    return render(request, 'main_page_app/sent.html', {})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
