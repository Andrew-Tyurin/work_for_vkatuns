from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.contrib import messages

from main.forms import MyResumeForm
from main.models import Resume
from main.utils import MyResumeMixin


class MyResumeView(MyResumeMixin, UpdateView):
    form_class = MyResumeForm
    template_name = 'main/myresume/myresume_edit_or_update.html'
    success_url = reverse_lazy('my_resume')

    def get_object(self, queryset=None):
        return self.kwargs['one_to_one_object']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            button='Сохранить',
            title_form='Изменить резюме',
            title='Моё резюме',
        )
        return context

    def get_success_url(self):
        messages.success(self.request, True)
        return self.success_url


class MyResumeStartView(MyResumeMixin, TemplateView):
    template_name = 'main/myresume/myresume_start.html'


class CreateMyResumeView(MyResumeMixin, CreateView):
    form_class = MyResumeForm
    template_name = 'main/myresume/myresume_edit_or_update.html'
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


class AllResumeView(ListView):
    model = Resume
    template_name = 'main/myresume/view_all_resume.html'

    def get_queryset(self):
        return super().get_queryset().select_related('specialty')
