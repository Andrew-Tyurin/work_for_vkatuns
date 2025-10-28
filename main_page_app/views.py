from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from main_page_app.forms import ApplicationForm
from user_company.models import Specialty, Company, Vacancy


class MainPageView(TemplateView):
    template_name = 'main_page_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty_list'] = Specialty.objects.annotate(count=Count('vacancies'))
        context['company_list'] = Company.objects.annotate(count=Count('vacancies'))
        return context


class AllVacanciesView(ListView):
    model = Vacancy
    template_name = 'main_page_app/vacancies.html'

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
    template_name = 'main_page_app/card_one_vacancy.html'
    model = Vacancy
    pk_url_kwarg = 'vacancy_id'

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied('403 - не авторизован')
        self.object = self.get_object()
        form = self.get_form()
        if request.user.applications.filter(vacancy=self.object):
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
    return render(request, 'main_page_app/sent.html', {})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка: 404 - страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка: 500 - проблема на сервере')
