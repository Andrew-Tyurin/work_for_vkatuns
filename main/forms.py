from django import forms
from django.core.exceptions import ValidationError

from main.models import Application, Company, Vacancy


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
                field.widget.attrs['class'] = 'form-control w-25'
                field.widget.attrs['placeholder'] = '8 *** *** ** **'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_written_cover_letter(self):
        written_cover_letter = self.cleaned_data['written_cover_letter']
        if len(written_cover_letter.strip()) < 15:
            raise ValidationError('Напишите подробней о себе')
        return written_cover_letter
