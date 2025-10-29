from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, TemplateView, CreateView

from user_company.forms import MyCompanyFrom, MyCompanyVacancyForm
from user_company.models import Vacancy
from user_company.utils import MyCompanyMixin


class MyCompanyStartView(MyCompanyMixin, TemplateView):
    template_name = 'user_company/mycompany_start.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = (
            f'Пока мы думаем, что вы – частное лицо.'
            f'Хотите создать карточку компании,'
            f'разместить информацию и вакансии?'
        )
        return context


class CreateMyCompanyView(MyCompanyMixin, CreateView):
    form_class = MyCompanyFrom
    template_name = 'user_company/mycompany_create.html'
    success_url = reverse_lazy('my_company')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyCompanyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyFrom
    template_name = 'user_company/mycompany.html'

    def get_object(self, queryset=None):
        return self.kwargs['user_company']

    def get_success_url(self):
        messages.success(self.request, True)
        return reverse_lazy('my_company')


class MyCompanyVacanciesListView(MyCompanyMixin, ListView):
    model = Vacancy
    template_name = 'user_company/mycompany_vacancies_list.html'

    def get_queryset(self):
        context = (
            self.kwargs['user_company'].vacancies.all()
            .values('id', 'title', 'salary_min', 'salary_max')
            .annotate(count_interested=Count('applications'))
        )
        return context


class CreateMyCompanyVacancyView(MyCompanyMixin, CreateView):
    form_class = MyCompanyVacancyForm
    template_name = 'user_company/mycompany_vacancy_create.html'
    success_url = reverse_lazy('my_company_vacancies_list')

    def form_valid(self, form):
        form.instance.company = self.kwargs['user_company']
        return super().form_valid(form)


class MyCompanyVacancyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyVacancyForm
    template_name = 'user_company/mycompany_vacancy.html'

    def get_object(self, queryset=None):
        company_vacancies = self.kwargs['user_company'].vacancies.all()
        return get_object_or_404(company_vacancies, id=self.kwargs['vacancy_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = context['object'].applications.all().values(
            'written_username',
            'written_phone',
            'written_cover_letter',
        )
        return context

    def get_success_url(self):
        messages.success(self.request, True)
        return reverse_lazy('my_company_vacancy', args=(self.kwargs['vacancy_id'],))
