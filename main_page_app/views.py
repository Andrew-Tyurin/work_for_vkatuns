from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Count
from . import models


def request_verification(name_patch, dynamic_path):
    """
        Проверяет, какой URL вызван, и возвращает объект из нужной модели по
        динамическому пути. Если объекта такого нету, то вызовется исключение
        DoesNotExist. Которые мы обработаем -> raise Http404. Exception нужен
        в случае если name_patch не соответсвует условиям, тогда функция
        request_verification вызвана с неправильными аргументами
    """
    try:

        if name_patch == 'vacancies_specialty':
            return models.Specialty.objects.get(code=dynamic_path)

        elif name_patch == 'companies_page':
            return models.Company.objects.get(id=dynamic_path)

        elif name_patch == 'one_vacancy':
            return models.Vacancy.objects.get(id=dynamic_path)

        raise Exception

    except ObjectDoesNotExist:
        # ObjectDoesNotExist - ловит всё семейство DoesNotExist(род класс)
        # models.Specialty.DoesNotExist - ловит исключение конкретной модели
        raise Http404


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
    # request.resolver_match.view_name - возвращает имя указанное в urls name="...."
    specialty_ru = request_verification(request.resolver_match.view_name, group_of_vacancies)
    vacancies = models.Vacancy.objects.filter(specialty=group_of_vacancies)

    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies, 'specialty_ru': specialty_ru},
    )


def companies_page(request, companies_id):
    company = request_verification(request.resolver_match.view_name, companies_id)
    vacancies = models.Vacancy.objects.filter(company_id=companies_id)

    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies, 'company': company},
    )


def one_vacancy(request, vacancy_id):
    vacancy_in_the_company = request_verification(request.resolver_match.view_name, vacancy_id)

    return render(
        request,
        'main_page_app/card_one_vacancy.html',
        {'vacancy_in_the_company': vacancy_in_the_company})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
