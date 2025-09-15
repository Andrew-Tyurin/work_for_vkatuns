from django.http import Http404
from django.shortcuts import render
from data import *


def vacancies_page(request):
    jobs_vacancies = jobs
    return render(request, 'vacancies_app/vacancies.html', {'jobs': jobs})


def one_vacancy(request, vacancies_id):
    return render(request, 'vacancies_app/card_one_vacancy.html', {})


def vacancies_specialty(request, specialty_request):
    specialty_ru = ''.join(c['title'] for c in specialties if c['code'] == specialty_request)

    if not specialty_ru:
        raise Http404
    jobs_specialty = list(filter(lambda vacancy: vacancy['specialty'] == specialty_request, jobs))

    return render(
        request,
        'vacancies_app/vacancies.html',
        {'jobs': jobs_specialty, 'specialty_ru': specialty_ru})
