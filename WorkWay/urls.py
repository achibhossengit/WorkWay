from django.contrib import admin
from django.urls import path, include
from api.views import root_redirect
from api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urls)),
    path('', root_redirect)
]