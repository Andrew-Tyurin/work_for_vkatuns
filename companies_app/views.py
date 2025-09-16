from django.shortcuts import render
from data import *


def companies_page(request, companies_id):
    companies_vacancies = list(filter(lambda job: int(job["company"]) == companies_id, jobs))
    company = companies[companies_id - 1]

    return render(
        request,
        'vacancies_app/vacancies.html',
        {
            'jobs': companies_vacancies, 'company': company}
    )
