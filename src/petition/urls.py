from django.urls import path, re_path

from . import views

app_name = "petition"

urlpatterns = [
    # Archive
    path("petition/archive/", views.Archive.as_view(), name="archive"),
    path(
        "petition/archive/export/", views.ArchiveExport.as_view(), name="export_archive"
    ),
    path(
        "petition/archive/import/", views.ArchiveImport.as_view(), name="import_archive"
    ),
    path(
        "petition/archive/chart1/",
        views.ArchiveChart1Export.as_view(),
        name="export_archive_chart_1",
    ),
    path(
        "petition/archive/chart2/",
        views.ArchiveChart2Export.as_view(),
        name="export_archive_chart_2",
    ),
    # Search
    path("search/", views.Search.as_view(), name="search"),
    # Petition
    path("petition/create/", views.PetitionCreate.as_view(), name="create"),
    path("petition/<int:id>/", views.PetitionDetail.as_view(), name="detail"),
    path("petition/<int:id>/vote/", views.PetitionVote.as_view(), name="vote"),
    # Petition news
    path(
        "petition/<int:petition_id>/news/create/",
        views.PetitionNewsCreate.as_view(),
        name="news_create",
    ),
    path(
        "petition/news/<int:id>/delete/",
        views.PetitionNewsDelete.as_view(),
        name="news_delete",
    ),
    re_path(r"^", views.Home.as_view(), name="home"),
]
