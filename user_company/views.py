from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, TemplateView, CreateView

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


class CreateMyCompanyView(MyCompanyMixin, CreateView):
    form_class = MyCompanyFrom
    template_name = 'user_company/mycompany_create.html'
    success_url = reverse_lazy('my_company')

    def dispatch(self, request, *args, **kwargs):
        if self.user_has_no_company(request.user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("403; Ваша компания уже зарегистрирована")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


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
                   .values('id', 'title', 'salary_min', 'salary_max', )
                   .annotate(count_interested=Count('applications'))
                   .filter(company=self.kwargs['user_company']))
        return context


class CreateMyCompanyVacancyView(MyCompanyMixin, CreateView):
    form_class = MyCompanyVacancyForm
    template_name = 'user_company/mycompany_vacancy_create.html'
    success_url = reverse_lazy('my_company_vacancies_list')

    def dispatch(self, request, *args, **kwargs):
        self.kwargs['user_company'] = self.user_has_companies(request.user)
        if self.kwargs['user_company'] is None:
            return redirect('my_company_start')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.company = self.kwargs['user_company']
        return super().form_valid(form)


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
