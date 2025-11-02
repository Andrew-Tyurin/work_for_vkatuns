from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ImproperlyConfigured
from django.shortcuts import redirect
from django.views import View


class OneToOneMixin(View):
    """
    Данный класс определяет может-ли авторизированный пользователь(объект User)
    иметь связь 'one to one' с объектами из других моделей, если
    связь имеется, то разрешаем взаимодействие пользователя со связанным объектом.
    Если нет объекта, то разрешаем создать связанный объект.

    my_object_settings - должен содержать имена ваших url,
    а их view - предполагает, что связанный объект уже
    существует и мы разрешаем с ним взаимодействовать(редактировать,
    добавлять новые связи, итд).

    create_my_object - должен содержать имена ваших url,
    а их view - предполагает, что связанный объект не существует
    и нужно его создать.
    """
    custom_raise_exception = True
    my_object_settings = None
    create_my_object = None

    def dispatch(self, request, *args, **kwargs):
        name_url_redirect = kwargs.get('name_url_redirect', 'main_page')
        text_raise = kwargs.get('text_raise', '403')
        object_attr = kwargs.get('object_attr', '')
        if request.resolver_match.url_name in self.my_object_settings:
            one_to_one_object = self.user_has_object(request.user, object_attr)
            if one_to_one_object is None:
                return redirect(name_url_redirect)
            self.kwargs['one_to_one_object'] = one_to_one_object
            return super().dispatch(request, *args, **kwargs)

        elif request.resolver_match.url_name in self.create_my_object:
            if self.user_has_no_object(request.user, object_attr):
                return super().dispatch(request, *args, **kwargs)
            raise PermissionDenied(text_raise)

        raise Exception("Что-то пошло не так на сервере")

    def raise_error_500(self, attr: str):
        raise ImproperlyConfigured(f"Поле '{attr}' отсутствует в модели User")

    def user_is_authenticated(self, user: User) -> User:
        if not user.is_authenticated and self.custom_raise_exception:
            raise PermissionDenied("403; Не авторизован")
        return user

    def user_has_object(self, user: User, attr: str) -> object | None:
        user = self.user_is_authenticated(user)
        try:
            one_to_one_object = getattr(user, attr)
        except ObjectDoesNotExist:
            return None
        except AttributeError:
            raise self.raise_error_500(attr)
        return one_to_one_object

    def user_has_no_object(self, user: User, attr: str) -> bool:
        user = self.user_is_authenticated(user)
        try:
            getattr(user, attr)
        except ObjectDoesNotExist:
            return True
        except AttributeError:
            raise self.raise_error_500(attr)
        return False


class MyCompanyMixin(OneToOneMixin):
    """ Связь пользователя с объектом Company """
    my_object_settings = ('my_company', 'my_company_vacancy', 'my_company_vacancies_list', 'create_vacancy_my_company')
    create_my_object = ('my_company_start', 'my_company_create')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(
            request,
            *args,
            name_url_redirect='my_company_start',
            text_raise='403; Ваша компания уже зарегистрирована',
            object_attr='owner',
            **kwargs
        )


class MyResumeMixin(OneToOneMixin):
    """ Связь пользователя с объектом Resume """
    my_object_settings = ('my_resume',)
    create_my_object = ('my_resume_create', 'my_resume_start')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(
            request,
            *args,
            name_url_redirect='my_resume_start',
            text_raise='403; У вас создано резюме',
            object_attr='my_resume',
            **kwargs
        )
