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
    path(
        "user/<int:id>/votes/",
        views.UserVotesList.as_view(),
        name="user_votes_list",
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
    re_path(r"statistics/0/", views.Statistics0.as_view(), name="statistics_0"),
    re_path(r"statistics/1/", views.Statistics1.as_view(), name="statistics_1"),
    re_path(r"statistics/2/", views.Statistics2.as_view(), name="statistics_2"),
    re_path(r"statistics/3/", views.Statistics3.as_view(), name="statistics_3"),
    re_path(r"statistics/4/", views.Statistics4.as_view(), name="statistics_4"),
    re_path(r"statistics/", views.Statistics.as_view(), name="statistics"),
    re_path(r"^", views.Home.as_view(), name="home"),
]
