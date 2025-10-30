from django import forms
from django.core.exceptions import ValidationError

from main.models import Application, Company, Vacancy, Resume


class MyCompanyFrom(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description')

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
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description')
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
                field.widget.attrs['rows'] = 3


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['written_username'].label = 'Вас зовут'
        for field_name, field in self.fields.items():
            if field_name == 'written_phone':
                field.widget.attrs = {'class': 'form-control w-25', 'placeholder': '8 *** *** ** **'}
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_written_cover_letter(self):
        written_cover_letter = self.cleaned_data['written_cover_letter']
        if len(written_cover_letter.strip()) < 15:
            raise ValidationError('Напишите подробней о себе')
        return written_cover_letter

class MyResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = (
            'name', 'surname', 'status',
            'salary', 'specialty', 'grade',
            'education', 'experience', 'portfolio'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialty'].empty_label = 'Выбрать...'
        for field_name, field in self.fields.items():
            if field_name in ('education', 'experience'):
                field.widget.attrs = {'class': 'form-control', 'rows': 4}
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.isalpha() and len(name) > 2:
            return name
        raise ValidationError('Имя должно из состоять минимум из двух букв')

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if surname.isalpha() and len(surname) > 2:
            return surname
        raise ValidationError('Фамилия должна состоять минимум из двух букв')

    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if int(salary) < 0:
            raise ValidationError('Вам должны платить, а не вы!')
        return salary

    def clean_portfolio(self):
        portfolio = self.cleaned_data['portfolio']
        if 'github.com' in portfolio or portfolio in '':
            return portfolio
        raise ValidationError('Неизвестный источник')
