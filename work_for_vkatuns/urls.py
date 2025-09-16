from django.urls import include, path
from django.contrib import admin
from main_page_app.views import custom_handler404, custom_handler500

handler500 = custom_handler500
handler404 = custom_handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page_app.urls')),
]
