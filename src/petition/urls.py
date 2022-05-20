from django.urls import path, re_path

from . import views

app_name = "petition"

urlpatterns = [
    path("petition/create/", views.PetitionCreate.as_view(), name="create"),
    path("petition/<int:id>/", views.PetitionDetail.as_view(), name="detail"),
    path("petition/<int:id>/vote/", views.PetitionVote.as_view(), name="vote"),
    re_path(r"^", views.Home.as_view(), name="home"),
]
