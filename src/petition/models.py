from django.db import models
from django.utils import timezone


class Petition(models.Model):
    title = models.TextField(
        verbose_name="Title",
        max_length=200,
        db_index=True,
        null=False,
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=2400,
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Date created",
        default=timezone.now,
        null=False,
    )
    author = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        verbose_name="Author",
        null=False,
    )
    votes_cache = models.PositiveIntegerField(
        verbose_name="Votes",
        blank=True,
        null=False,
        default=0,
    )

    class Meta:
        verbose_name = "Petition"
        verbose_name_plural = "Petitions"
        db_table = "petition_petition"


class Vote(models.Model):
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        null=False,
        verbose_name="User",
    )
    petition = models.ForeignKey(
        "petition.Petition",
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Petition",
    )
    reason = models.TextField(
        verbose_name="Reason",
        max_length=400,
        null=True,
        blank=True,
        default=None,
    )
    created_at = models.DateTimeField(
        verbose_name="Date created",
        default=timezone.now,
        null=False,
    )

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        db_table = "petition_vote"


class PetitionNews(models.Model):
    petition = models.ForeignKey(
        "petition.Petition",
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Petition",
    )
    title = models.TextField(
        verbose_name="Title",
        max_length=200,
        db_index=True,
        null=False,
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=2400,
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Date created",
        default=timezone.now,
        null=False,
    )

    class Meta:
        verbose_name = "Petition News"
        verbose_name_plural = "Petition News"
        db_table = "petition_news"


class PetitionNotification(models.Model):

    petition = models.ForeignKey(
        "petition.Petition",
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Petition",
    )
    title = models.TextField(
        verbose_name="Title",
        max_length=40,
        db_index=True,
        null=False,
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=300,
        null=False,
    )
    path = models.TextField(
        verbose_name="Reference path",
        max_length=240,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Date created",
        default=timezone.now,
        null=False,
    )

    class Meta:
        verbose_name = "Petition News"
        verbose_name_plural = "Petition News"
        db_table = "petition_news"
