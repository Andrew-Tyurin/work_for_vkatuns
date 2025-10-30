from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from main.forms import ApplicationForm, MyCompanyFrom, MyCompanyVacancyForm, MyResumeForm
from main.models import Specialty, Company, Vacancy
from main.utils import MyCompanyMixin, MyResumeMixin


class MainPageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty_list'] = Specialty.objects.annotate(count=Count('vacancies'))
        context['company_list'] = Company.objects.annotate(count=Count('vacancies'))
        return context


class AllVacanciesView(ListView):
    model = Vacancy
    template_name = 'main/vacancies.html'

    def get_queryset(self):
        return super().get_queryset().select_related('company')


class VacanciesBySpecialtyView(AllVacanciesView, ListView):
    allow_empty = True

    def get_queryset(self):
        specialty = self.kwargs['specialty_slug']
        return Vacancy.objects.filter(specialty=specialty).select_related('company')

    def get_context_data(self, **kwargs):
        specialty = get_object_or_404(Specialty, code=self.kwargs['specialty_slug'])
        return super().get_context_data(specialty_ru=specialty.title, **kwargs)


class VacanciesByCompaniesView(AllVacanciesView, ListView):
    allow_empty = True

    def get_queryset(self):
        company = self.kwargs['company_id']
        return Vacancy.objects.filter(company=company).select_related('company')

    def get_context_data(self, **kwargs):
        company = get_object_or_404(Company, id=self.kwargs['company_id'])
        return super().get_context_data(company=company, **kwargs)


class OneVacancyView(FormMixin, DetailView):
    form_class = ApplicationForm
    template_name = 'main/card_one_vacancy.html'
    model = Vacancy
    pk_url_kwarg = 'vacancy_id'

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied('403 - не авторизован')
        self.object = self.get_object()
        form = self.get_form()
        if request.user.applications.filter(vacancy=self.object).exists():
            form.add_error(None, 'Вы уже откликнулись на эту вакансию')
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.vacancy = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('send_application', args=(self.kwargs['vacancy_id'],))


def send_application(request, vacancy_id):
    return render(request, 'main/sent.html', {})


class MyCompanyStartView(MyCompanyMixin, TemplateView):
    template_name = 'main/mycompany_start.html'

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
    template_name = 'main/mycompany_create.html'
    success_url = reverse_lazy('my_company')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyCompanyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyFrom
    template_name = 'main/mycompany.html'

    def get_object(self, queryset=None):
        return self.kwargs['user_company']

    def get_success_url(self):
        messages.success(self.request, True)
        return reverse_lazy('my_company')


class MyCompanyVacanciesListView(MyCompanyMixin, ListView):
    model = Vacancy
    template_name = 'main/mycompany_vacancies_list.html'

    def get_queryset(self):
        context = (
            self.kwargs['user_company'].vacancies.all()
            .values('id', 'title', 'salary_min', 'salary_max')
            .annotate(count_interested=Count('applications'))
        )
        return context


class CreateMyCompanyVacancyView(MyCompanyMixin, CreateView):
    form_class = MyCompanyVacancyForm
    template_name = 'main/mycompany_vacancy_create.html'
    success_url = reverse_lazy('my_company_vacancies_list')

    def form_valid(self, form):
        form.instance.company = self.kwargs['user_company']
        return super().form_valid(form)


class MyCompanyVacancyView(MyCompanyMixin, UpdateView):
    form_class = MyCompanyVacancyForm
    template_name = 'main/mycompany_vacancy.html'

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


class MyResumeView(MyResumeMixin, UpdateView):
    form_class = MyResumeForm
    template_name = 'main/myresume_edit_or_update.html'
    success_url = reverse_lazy('my_resume')

    def get_object(self, queryset=None):
        return self.kwargs['user_resume']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            button='Сохранить',
            title_form='Изменить резюме',
            title='Моё резюме',
        )
        return context


class MyResumeStartView(MyResumeMixin, TemplateView):
    template_name = 'main/myresume_start.html'


class CreateMyResumeView(MyResumeMixin, CreateView):
    form_class = MyResumeForm
    template_name = 'main/myresume_edit_or_update.html'
    success_url = reverse_lazy('my_resume')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            button='Создать',
            title_form='Создать резюме',
            title='Создание резюме',
        )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
