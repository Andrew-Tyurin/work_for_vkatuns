from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from user_company.models import Company


class MyCompanyMixin:
    """
    Данный класс помогает работать с доступами
    пользователй для приложения user_company.
    """
    custom_raise_exception = True

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
