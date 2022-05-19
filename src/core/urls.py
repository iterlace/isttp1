from account import urls as account_urls
from petition import urls as petition_urls

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include(account_urls, namespace="account"), name="account"),
    re_path("^", include(petition_urls, namespace="petition"), name="petition"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
