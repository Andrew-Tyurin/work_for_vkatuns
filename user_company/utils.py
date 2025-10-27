from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from user_company.models import Company


class MyCompanyMixin:
    def user_has_companies(self, user: User) -> Company:
        if user.is_anonymous:
            raise PermissionDenied("403; Не авторизирован")
        try:
            user_company = user.owner
        except ObjectDoesNotExist:
            return None
        return user_company

    def user_has_no_company(self, user: User) -> bool:
        if user.is_anonymous:
            raise PermissionDenied("403; Не авторизирован")
        try:
            user.owner
        except ObjectDoesNotExist:
            return True
        return False
