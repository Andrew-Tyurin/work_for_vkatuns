from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.forms import RegisterUserFrom, LoginUserForm
from user.utils import DecorativeMixin


class LoginUserView(DecorativeMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'user/register_login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied('Вы уже авторизированны')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_elements(
            button='Войти',
            title_form='Войти, чтобы управлять',
        ))
        return context

    def get_success_url(self):
        return reverse_lazy('main_page')


class RegisterUserView(DecorativeMixin, CreateView):
    template_name = 'user/register_login.html'
    form_class = RegisterUserFrom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_elements(
            button='Зарегистрироваться',
            title_form='Создать аккаунт',
        ))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main_page')


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('main_page')
