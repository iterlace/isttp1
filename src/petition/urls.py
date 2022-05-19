from django.urls import path, re_path

from . import views

app_name = "petition"

urlpatterns = [
    re_path(r"^", views.Home.as_view(), name="home"),
]
