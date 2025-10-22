from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from main_page_app.views import custom_handler404, custom_handler500

from . import settings

handler500 = custom_handler500
handler404 = custom_handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)