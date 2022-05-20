import logging
import re
import uuid
from typing import List, Optional

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserQuerySet(models.QuerySet):
    pass


class UserManager(
    models.manager.BaseManager.from_queryset(UserQuerySet),
    BaseUserManager,
):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create and save an User with the given phone and password.
        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.User user: user
        :raises ValueError: phone is not set
        """
        now = timezone.now()
        if not email:
            raise ValueError("The email is not set!")

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name="E-Mail", unique=True)

    first_name = models.TextField(verbose_name="First Name", max_length=64)

    last_name = models.TextField(verbose_name="Last Name", max_length=64)

    date_joined = models.DateTimeField("Date joined", default=timezone.now)

    is_staff = models.BooleanField("Is admin", default=False)

    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "account_user"

    @property
    def full_name(self):
        return "{} {}".format(self.first_name.title(), self.last_name.title())

    @property
    def initials(self):
        return "{} {}.".format(self.last_name.title(), self.first_name[0].capitalize())
