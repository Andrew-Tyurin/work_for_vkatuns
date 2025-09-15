from django.shortcuts import render
from data import *
from django.http import HttpResponseNotFound, HttpResponseServerError


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


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
