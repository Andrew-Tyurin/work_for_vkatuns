from django.urls import path
from . import views

urlpatterns = [
    path('<int:companies_id>', views.companies_page, name='companies_page'),
]
