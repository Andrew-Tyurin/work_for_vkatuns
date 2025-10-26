from django.db.models import Count
from django.shortcuts import render
from django.views.generic import UpdateView, ListView

from user_company.forms import MyCompanyFrom, MyCompanyVacancyForm
from user_company.models import Company, Vacancy


def my_company_start(request):
    return render(request, 'user_company/mycompany_start.html', {})


def my_company_create(request):
    return render(request, 'user_company/mycompany_create.html', {})


class MyCompanyView(UpdateView):
    form_class = MyCompanyFrom
    template_name = 'user_company/mycompany.html'

    def get_object(self, queryset=None):
        return Company.objects.get(owner=self.request.user)


class MyCompanyVacanciesListView(ListView):
    model = Vacancy
    template_name = 'user_company/mycompany_vacancies_list.html'

    def get_queryset(self):
        context = (Vacancy.objects
                   .values('id', 'title', 'salary_min', 'salary_max',)
                   .annotate(count_interested=Count('applications'))
                   .filter(company=self.request.user.owner))
        return context


def create_vacancy_my_company(request):
    return render(request, 'user_company/mycompany_vacancy_create.html', {})


class MyCompanyVacancyView(UpdateView):
    form_class = MyCompanyVacancyForm
    template_name = 'user_company/mycompany_vacancy.html'

    def get_object(self, queryset=None):
        objects = self.request.user.owner.vacancies.get(id=self.kwargs['vacancy_id'])
        return objects
