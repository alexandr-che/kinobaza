from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from kinobaza import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls', namespace='movies'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
