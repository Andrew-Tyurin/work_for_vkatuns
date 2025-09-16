from django.shortcuts import render
from data import *
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404


def main_page(request):
    return render(
        request,
        'main_page_app/index.html',
        {
            'specialties': specialties,
            'companies': companies,
            'jobs': jobs,
        }
    )


def vacancies_specialty(request, specialty_request):
    specialty_ru = ''.join(c['title'] for c in specialties if c['code'] == specialty_request)
    if not specialty_ru:
        raise Http404
    jobs_specialty = list(filter(lambda vacancy: vacancy['specialty'] == specialty_request, jobs))

    return render(
        request,
        'main_page_app/vacancies.html',
        {'jobs': jobs_specialty, 'specialty_ru': specialty_request})


def vacancies_page(request):
    return render(request, 'main_page_app/vacancies.html', {'jobs': jobs})


def one_vacancy(request, vacancy_id):
    try:
        job = jobs[vacancy_id - 1]
        vacancy_in_the_company = companies[int(job['company']) - 1]
    except (KeyError, IndexError):
        raise Http404

    return render(
        request,
        'main_page_app/card_one_vacancy.html',
        {'job': job, 'company': vacancy_in_the_company})


def companies_page(request, companies_id):
    try:
        companies_vacancies = list(filter(lambda job: int(job["company"]) == companies_id, jobs))
        company = companies[companies_id - 1]
    except (KeyError, IndexError):
        raise Http404

    return render(
        request,
        'main_page_app/vacancies.html',
        {
            'jobs': companies_vacancies, 'company': company}
    )


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
