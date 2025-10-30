from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import redirect
from django.views import View

from main.models import Company, Resume


class MyCompanyMixin(View):
    """
    Данный класс помогает работать с доступами пользователй к
    разным url связанные с созданием или работой уже текущей компании.
    """
    custom_raise_exception = True
    CREATE_MY_COMPANY = ('my_company_start', 'my_company_create')
    MY_COMPANY_SETTINGS = ('my_company', 'my_company_vacancy', 'my_company_vacancies_list', 'create_vacancy_my_company')

    def dispatch(self, request, *args, **kwargs):
        if request.resolver_match.url_name in self.MY_COMPANY_SETTINGS:
            self.kwargs['user_company'] = self.user_has_companies(request.user)
            if self.kwargs['user_company'] is None:
                return redirect('my_company_start')
            return super().dispatch(request, *args, **kwargs)

        elif request.resolver_match.url_name in self.CREATE_MY_COMPANY:
            if self.user_has_no_company(request.user):
                return super().dispatch(request, *args, **kwargs)
            raise PermissionDenied("403; Ваша компания уже зарегистрирована")

        raise Exception("Что-то пошло не так на сервере")

    def user_is_authenticated(self, user: User) -> User:
        if not user.is_authenticated and self.custom_raise_exception:
            raise PermissionDenied("403; Не авторизован")
        return user

    def user_has_companies(self, user: User) -> Company | None:
        user = self.user_is_authenticated(user)
        try:
            user_company = user.owner
        except ObjectDoesNotExist:
            return None
        return user_company

    def user_has_no_company(self, user: User) -> bool:
        user = self.user_is_authenticated(user)
        try:
            user.owner
        except ObjectDoesNotExist:
            return True
        return False


class MyResumeMixin(View):
    """
    Данный класс помогает работать с доступами пользователй
    к разным url связанные созданием или обновлением своего резюме.
    """
    custom_raise_exception = True
    CREATE_MY_RESUME = ('my_resume_create', 'my_resume_start')
    MY_RESUME_SETTINGS = ('my_resume',)

    def dispatch(self, request, *args, **kwargs):
        if request.resolver_match.url_name in self.MY_RESUME_SETTINGS:
            self.kwargs['user_resume'] = self.user_has_resume(request.user)
            if self.kwargs['user_resume'] is None:
                return redirect('my_resume_start')
            return super().dispatch(request, *args, **kwargs)

        elif request.resolver_match.url_name in self.CREATE_MY_RESUME:
            if self.user_has_no_resume(request.user):
                return super().dispatch(request, *args, **kwargs)
            raise PermissionDenied("403; У вас создано резюме")

        raise Exception("Что-то пошло не так на сервере")

    def user_has_resume(self, user: User) -> Resume | None:
        user = MyCompanyMixin.user_is_authenticated(self, user)
        try:
            user_resume = user.my_resume
        except ObjectDoesNotExist:
            return None
        return user_resume

    def user_has_no_resume(self, user: User) -> bool:
        user = MyCompanyMixin.user_is_authenticated(self, user)
        try:
            user.my_resume
        except ObjectDoesNotExist:
            return True
        return False
