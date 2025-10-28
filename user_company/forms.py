from django import forms

from user_company.models import Company, Vacancy


class MyCompanyFrom(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name_field, field in self.fields.items():
            if name_field == 'logo':
                field.widget = forms.FileInput(attrs={})
            else:
                field.widget.attrs['class'] = 'form-control'
                if name_field == 'description':
                    field.widget.attrs['rows'] = 4


class MyCompanyVacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description',)
        labels = {
            'title': 'Название вакансии',
            'skills': 'Требуемые навыки',
            'description': 'Описание вакансии',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialty'].empty_label = 'Выбрать...'
        for name_field, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                if name_field == 'skills':
                    field.widget.attrs['rows'] = 3 # поля класса TextField в html(<textarea>) высоту и ширину изменяет атрибуты rows/cols
