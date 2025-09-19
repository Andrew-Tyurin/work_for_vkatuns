from django.http import HttpResponseNotFound, HttpResponseServerError, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from . import models


def main_page(request: HttpRequest) -> HttpResponse:
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


def vacancies_page(request: HttpRequest) -> HttpResponse:
    vacancies = models.Vacancy.objects.all()

    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies},
    )


def vacancies_specialty(request: HttpRequest, group_of_vacancies: str) -> HttpResponse:
    # request.resolver_match.view_name - возвращает имя указанное в urls name="...."
    specialty_ru = get_object_or_404(models.Specialty, code=group_of_vacancies)
    vacancies = models.Vacancy.objects.filter(specialty=group_of_vacancies)

    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies, 'specialty_ru': specialty_ru},
    )


def companies_page(request: HttpRequest, companies_id: int) -> HttpResponse:
    company = get_object_or_404(models.Company, id=companies_id)
    vacancies = models.Vacancy.objects.filter(company_id=companies_id)

    return render(
        request,
        'main_page_app/vacancies.html',
        {'vacancies': vacancies, 'company': company},
    )


def one_vacancy(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    vacancy_in_the_company = get_object_or_404(models.Vacancy, id=vacancy_id)

    return render(
        request,
        'main_page_app/card_one_vacancy.html',
        {'vacancy_in_the_company': vacancy_in_the_company})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
