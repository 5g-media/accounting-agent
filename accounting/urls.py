"""accounting URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin

from api.urls import api_urlpatterns, api_version

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/{}/'.format(api_version), include(api_urlpatterns, namespace=api_version)),
]
