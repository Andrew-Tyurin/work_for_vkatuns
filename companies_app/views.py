from django.shortcuts import render


def companies_page(request, companies_id):
    return render(request, 'companies_app/companies.html', {})
