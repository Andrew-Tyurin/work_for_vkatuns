from django.shortcuts import render
from . import models
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404


def main_page(request):
    specialty_list = models.Specialty.objects.annotate(count=Count('vacancies'))
    company_list = models.Company.objects.annotate(count=Count('vacancies'))
    return render(
        request,
        'main_page_app/index.html',
        {
            'specialty_list': specialty_list,
            'company_list': company_list,
        },
    )


def vacancies_page(request):
    vacancies = models.Vacancy.objects.all()
    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies},
    )


def vacancies_specialty(request, group_of_vacancies):
    try:
        specialty_ru = models.Specialty.objects.get(code=group_of_vacancies)
    except models.Specialty.DoesNotExist:
        raise Http404
    vacancies = models.Vacancy.objects.filter(specialty=group_of_vacancies)

    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies, 'specialty_ru': specialty_ru},
    )


def companies_page(request, companies_id):
    try:
        company = models.Company.objects.get(id=companies_id)
    except models.Company.DoesNotExist:
        raise Http404
    vacancies = models.Vacancy.objects.filter(company_id=companies_id)

    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies, 'company': company},
    )


def one_vacancy(request, vacancy_id):
    try:
        vacancy_in_the_company = models.Vacancy.objects.get(id=vacancy_id)
    except models.Vacancy.DoesNotExist:
        raise Http404

    return render(
        request,
        'main_page_app/card_one_vacancy.html',
        {'vacancy_in_the_company': vacancy_in_the_company})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
