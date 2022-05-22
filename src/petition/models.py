import math

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
        related_name="owned_petitions",
    )
    signatories = models.ManyToManyField(
        "account.User",
        through="petition.Vote",
        related_name="signed_petitions",
    )
    # Votes cached quantity
    signatories_count = models.PositiveIntegerField(
        verbose_name="Votes",
        blank=True,
        null=False,
        default=0,
    )

    def __str__(self):
        return self.title

    @property
    def signatories_goal(self):
        return 2 ** (math.floor(math.sqrt(self.signatories_count + 1)) + 1)

    @property
    def signatories_percentage(self):
        return math.floor(self.signatories_count / self.signatories_goal * 100)

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
        related_name="votes",
    )
    petition = models.ForeignKey(
        "petition.Petition",
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Petition",
        related_name="votes",
    )

    # TODO: remove?
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
        related_name="news",
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
        ordering = ("-created_at",)


class Notification(models.Model):
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        null=False,
        verbose_name="User",
        related_name="notifications",
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
        db_table = "petition_notifications"
        ordering = ("-created_at",)
