from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, ListView, TemplateView

from user_company.forms import MyCompanyFrom, MyCompanyVacancyForm
from user_company.models import Vacancy
from user_company.utils import MyCompanyMixin


class MyCompanyStartView(MyCompanyMixin, TemplateView):
    template_name = 'user_company/mycompany_start.html'

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_no_company(request.user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("403; Ваша компания уже зарегистрирована")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = (
            f'Пока мы думаем, что вы – частное лицо.'
            f'Хотите создать карточку компании,'
            f'разместить информацию и вакансии?'
        )
        return context


def my_company_create(request):
    return render(request, 'user_company/mycompany_create.html', {})


class MyCompanyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyFrom
    template_name = 'user_company/mycompany.html'

    def dispatch(self, request, *args, **kwargs):
        self.kwargs['user_company'] = self.user_has_companies(request.user)
        if self.kwargs['user_company'] is None:
            return redirect('my_company_start')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.kwargs['user_company']


class MyCompanyVacanciesListView(MyCompanyMixin, ListView):
    model = Vacancy
    template_name = 'user_company/mycompany_vacancies_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.kwargs['user_company'] = self.user_has_companies(request.user)
        if self.kwargs['user_company'] is None:
            return redirect('my_company_start')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        context = (Vacancy.objects
                   .values('id', 'title', 'salary_min', 'salary_max',)
                   .annotate(count_interested=Count('applications'))
                   .filter(company=self.kwargs['user_company']))
        return context


def create_vacancy_my_company(request):
    return render(request, 'user_company/mycompany_vacancy_create.html', {})


class MyCompanyVacancyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyVacancyForm
    template_name = 'user_company/mycompany_vacancy.html'

    def dispatch(self, request, *args, **kwargs):
        self.kwargs['user_company'] = self.user_has_companies(request.user)
        if self.kwargs['user_company'] is None:
            return redirect('my_company_start')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        company_vacancies = self.request.user.owner.vacancies.all()
        return get_object_or_404(company_vacancies, id=self.kwargs['vacancy_id'])
