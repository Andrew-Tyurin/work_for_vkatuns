from django.shortcuts import render


def my_company_start(request):
    return render(request, 'user_company/mycompany_start.html', {})

def my_company_create(request):
    return render(request, 'user_company/mycompany_create.html', {})


def my_company(request):
    return render(request, 'user_company/mycompany.html', {})


def my_company_vacancies_list(request):
    return render(request, 'user_company/mycompany_vacancies_list.html', {})


def create_vacancy_my_company(request):
    return render(request, 'user_company/mycompany_vacancy_create.html', {})

def my_company_vacancy(request, vacancy_id):
    return render(request, 'user_company/mycompany_vacancy.html', {})
