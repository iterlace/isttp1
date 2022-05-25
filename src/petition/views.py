import io
from typing import List

import xlsxwriter
from pygooglechart import PieChart2D

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView

from account.models import User
from petition.models import Petition, PetitionNews, Vote

from .forms import PetitionCreateForm, PetitionNewsCreateForm


class Home(TemplateView):
    template_name = "home.html"

    def get_owned_petitions(self) -> List[Petition]:
        if not self.request.user.is_authenticated:
            return []

        return list(self.request.user.owned_petitions.all())

    def get_signed_petitions(self) -> List[Petition]:
        if not self.request.user.is_authenticated:
            return []

        return list(self.request.user.signed_petitions.all())

    def get_trending_petitions(self) -> List[Petition]:
        limit = 20

        petitions = Petition.objects.filter(
            created_at__gt=timezone.now() - timezone.timedelta(days=14),
        ).order_by("-signatories_count")
        return list(petitions[:limit])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["signed_petitions"] = self.get_signed_petitions()
        ctx["trending_petitions"] = self.get_trending_petitions()
        ctx["owned_petitions"] = self.get_owned_petitions()
        return ctx


class Archive(TemplateView):
    template_name = "petition/archive.html"

    def get_petitions(self) -> List[Petition]:
        petitions = Petition.objects.all().order_by("-created_at")
        return list(petitions)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["petitions"] = self.get_petitions()
        return ctx


class ArchiveExport(View):
    def get_file(self) -> bytes:
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        petitions_ws = workbook.add_worksheet(name="Petitions List")

        petitions = Petition.objects.all().order_by("-created_at")

        petitions_ws.add_table(
            f"B2:F{2+len(petitions)}",
            {
                "columns": [
                    {"header": "Title"},
                    {"header": "Description"},
                    {"header": "Created At"},
                    {"header": "Author"},
                    {"header": "Signatories"},
                ]
            },
        )
        petitions_ws.set_column("B:C", 40)  # set width
        petitions_ws.set_column("D:F", 20)  # set width

        for idx, petition in enumerate(petitions, start=3):
            petitions_ws.write(f"B{idx}", petition.title)
            petitions_ws.write(f"C{idx}", petition.description)
            petitions_ws.write(f"D{idx}", petition.created_at.strftime("%d.%m.%Y"))
            petitions_ws.write(f"E{idx}", petition.author.full_name)
            petitions_ws.write(f"F{idx}", str(petition.signatories_count))

            signatories_ws = workbook.add_worksheet(name=petition.title[:31])

            votes = petition.votes.select_related("user").order_by("-created_at")
            signatories_ws.add_table(
                f"B2:C{2+len(votes)}",
                {
                    "columns": [
                        {"header": "Full name"},
                        {"header": "Sign date"},
                    ]
                },
            )
            signatories_ws.set_column("B:B", 30)  # set width
            signatories_ws.set_column("C:C", 15)  # set width

            for idx, vote in enumerate(votes, start=3):
                signatories_ws.write(f"B{idx}", vote.user.full_name)
                signatories_ws.write(f"C{idx}", vote.created_at.strftime("%d.%m.%Y"))
        workbook.close()

        buffer.seek(0)
        return buffer.read()

    def get(self, request, **kwargs):
        file = self.get_file()
        response = HttpResponse(
            file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=archive.xlsx"
        return response


class ArchiveChartExport(View):
    def get_file(self) -> bytes:
        colours = ["3374cd", "992220", "469b57", "e4e144", "cd3333", "749920"]
        since = timezone.now() - timezone.timedelta(days=14)
        petitions = (
            Petition.objects.filter(created_at__gte=since)
            .order_by("-signatories_count")
            .values("signatories_count", "title")[:5]
        )

        chart = PieChart2D(750, 400)
        chart.title = "Most voted petitions (created since {})".format(
            since.strftime("%d.%m.%Y")
        )
        chart.add_data([i["signatories_count"] for i in petitions])
        chart.set_pie_labels([i["title"] for i in petitions])
        chart.set_colours(colours[: len(petitions)])

        buffer = chart.download()
        return buffer

    def get(self, request, **kwargs):
        file = self.get_file()
        response = HttpResponse(
            file,
            content_type="image/png",
        )
        response["Content-Disposition"] = "attachment; filename=chart.png"
        return response


class PetitionCreate(LoginRequiredMixin, CreateView):
    model = Petition
    form_class = PetitionCreateForm
    template_name = "petition/create.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("petition:detail", kwargs={"id": self.object.pk})

    def form_valid(self, form):
        form.instance.author_id = self.request.user.pk
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class PetitionDetail(DetailView):
    model = Petition
    template_name = "petition/detail.html"
    pk_url_kwarg = "id"

    def get_is_owner(self):
        return self.request.user.pk == self.object.author_id

    def get_already_signed(self):
        return self.object.signatories.filter(pk=self.request.user.pk).exists()

    def get_latest_votes(self):
        return self.object.votes.order_by("-created_at")

    def get_news(self):
        return self.object.news.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["is_owner"] = self.get_is_owner()
        ctx["already_signed"] = self.get_already_signed()
        ctx["latest_votes"] = self.get_latest_votes()
        ctx["news"] = self.get_news()
        return ctx


class PetitionVote(LoginRequiredMixin, DetailView):
    model = Petition
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        petition = self.get_object()
        user = self.request.user
        Vote.objects.get_or_create(
            petition_id=petition.pk, user_id=user.pk, defaults={}
        )
        return redirect("petition:detail", id=petition.pk)


class PetitionNewsCreate(LoginRequiredMixin, CreateView):
    model = PetitionNews
    form_class = PetitionNewsCreateForm
    template_name = "petition_news/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.petition = Petition.objects.filter(
            pk=self.kwargs["petition_id"],
            author_id=self.request.user.pk,
        ).first()
        if self.petition is None:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["petition"] = self.petition
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("petition:detail", kwargs={"id": self.object.petition.pk})

    def form_valid(self, form):
        form.instance.petition_id = self.petition.pk
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class PetitionNewsDelete(LoginRequiredMixin, DeleteView):
    model = PetitionNews
    pk_url_kwarg = "id"

    def dispatch(self, request, *args, **kwargs):
        self.petition = Petition.objects.filter(
            news__id=self.kwargs["id"],
            author_id=self.request.user.pk,
        ).first()
        if self.petition is None:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("petition:detail", kwargs={"id": self.petition.pk})

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def form_valid(self, form):
        form.instance.author_id = self.request.user.pk
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
