from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page_app.urls')),
    path('vacancies/', include('vacancies_app.urls')),
    path('companies/', include('companies_app.urls')),
]
