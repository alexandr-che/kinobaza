from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import debug_toolbar

from kinobaza import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls', namespace='movies')),
    path('user/', include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
