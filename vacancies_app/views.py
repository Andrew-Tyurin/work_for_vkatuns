from django.shortcuts import render


def vacancies_page(request):
    return render(request, 'vacancies_app/vacancies.html', {})


def one_vacancy(request, vacancies_id):
    return render(request, 'vacancies_app/card_one_vacancy.html', {})


def vacancies_specialty(request, specialty):
    return render(request, 'vacancies_app/vacancies_by_specialty.html', {})
