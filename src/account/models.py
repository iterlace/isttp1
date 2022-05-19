import logging
import re
import uuid
from typing import List, Optional

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Greatest, Upper
from django.db.models.indexes import Index
from django.utils import timezone
from django.utils.html import format_html
from django.utils.timezone import timedelta
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name="E-Mail", unique=True)

    first_name = models.TextField(verbose_name="First Name", max_length=64)

    last_name = models.TextField(verbose_name="Last Name", max_length=64)

    date_joined = models.DateTimeField("Date joined", default=timezone.now)

    is_admin = models.BooleanField("Is admin", default=False)

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "account_user"
