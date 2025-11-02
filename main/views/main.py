from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, QuerySet, Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from main.forms import ApplicationForm, SearchForm
from main.models import Specialty, Company, Vacancy


class MainPageView(TemplateView):
    template_name = 'main/main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty_list'] = Specialty.objects.annotate(count=Count('vacancies'))
        context['company_list'] = Company.objects.annotate(count=Count('vacancies'))
        context['form'] = SearchForm()
        return context


class AllVacanciesView(ListView):
    model = Vacancy
    template_name = 'main/main/vacancies.html'

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


class SearchVacanciesView(ListView):
    template_name = 'main/main/vacancies.html'
    model = Vacancy

    def get_queryset(self, **kwargs):
        query_key = self.request.GET.get('s')
        if isinstance(query_key, str):
            query_key = query_key.strip()
        if query_key is None or query_key == '':
            queryset = None
        else:
            queryset = self.model.objects.filter(Q(title__icontains=query_key) | Q(skills__icontains=query_key))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.object_list and isinstance(self.object_list, QuerySet):
            context['empty_object_list'] = 'Ничего не найдено'
        elif self.object_list is None:
            context['non_object_list'] = 'Начать поиск!!!'
        context['search'] = True
        context['form'] = SearchForm()
        return context


class OneVacancyView(FormMixin, DetailView):
    form_class = ApplicationForm
    template_name = 'main/main/card_one_vacancy.html'
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


def send_application(request: HttpRequest, vacancy_id) -> HttpResponse:
    return render(request, 'main/main/send.html', {})
