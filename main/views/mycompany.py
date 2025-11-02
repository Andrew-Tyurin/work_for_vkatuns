from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.contrib import messages

from main.forms import MyCompanyFrom, MyCompanyVacancyForm
from main.models import Vacancy
from main.utils import MyCompanyMixin


class MyCompanyStartView(MyCompanyMixin, TemplateView):
    template_name = 'main/mycompany/mycompany_start.html'

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
    template_name = 'main/mycompany/mycompany_create.html'
    success_url = reverse_lazy('my_company')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyCompanyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyFrom
    template_name = 'main/mycompany/mycompany.html'

    def get_object(self, queryset=None):
        return self.kwargs['one_to_one_object']

    def get_success_url(self):
        messages.success(self.request, True)
        return reverse_lazy('my_company')


class MyCompanyVacanciesListView(MyCompanyMixin, ListView):
    model = Vacancy
    template_name = 'main/mycompany/mycompany_vacancies_list.html'

    def get_queryset(self):
        context = (
            self.kwargs['one_to_one_object'].vacancies
            .values('id', 'title', 'salary_min', 'salary_max')
            .annotate(count_interested=Count('applications'))
        )
        return context


class CreateMyCompanyVacancyView(MyCompanyMixin, CreateView):
    form_class = MyCompanyVacancyForm
    template_name = 'main/mycompany/mycompany_vacancy_create.html'
    success_url = reverse_lazy('my_company_vacancies_list')

    def form_valid(self, form):
        form.instance.company = self.kwargs['one_to_one_object']
        return super().form_valid(form)


class MyCompanyVacancyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyVacancyForm
    template_name = 'main/mycompany/mycompany_vacancy.html'

    def get_object(self, queryset=None):
        company_vacancies = self.kwargs['one_to_one_object'].vacancies.all()
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
