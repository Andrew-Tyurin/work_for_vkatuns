from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import redirect
from django.views import View

from user_company.models import Company


class MyCompanyMixin(View):
    """
    Данный класс помогает работать с доступами
    пользователй к разным url приложения user_company.
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
