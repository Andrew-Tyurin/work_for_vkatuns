from django.contrib import admin
from django.utils.safestring import mark_safe

from main_page_app.models import Company, Vacancy, Specialty


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'show_logo')

    def show_logo(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" alt="logo" width="50"/>')

    show_logo.short_description = 'логотип'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'specialty',
        'title',
        'salary_avg',
        'published_at',
        'company_name',
        'show_logo_company',
    )

    def show_logo_company(self, obj):
        return mark_safe(f'<img src="{obj.company.logo.url}" alt="logo" width="50"/>')

    show_logo_company.short_description = 'логотип компании'

    def salary_avg(self, obj):
        return f'{int(obj.salary_max + obj.salary_min) / 2:,} Р'

    salary_avg.short_description = 'средняя зарплата'

    def company_name(self, obj):
        return obj.company.name

    company_name.short_description = 'название компании'


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title', 'picture_speciality')

    def picture_speciality(self, obj):
        return mark_safe(f'<img src="{obj.picture.url}" alt="picture" width="35"/>')

    picture_speciality.short_description = 'картинка вакансии'