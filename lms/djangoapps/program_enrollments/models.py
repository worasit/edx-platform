# -*- coding: utf-8 -*-
"""
Django model specifications for the Program Enrollments API
"""
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class ProgramEnrollment(TimeStampedModel):  # pylint: disable=model-missing-unicode
    """
    This is a model for Program Enrollments from the registrar service

    .. pii: PII is found in the email address and the external key for a program enrollment
    .. pii_types: email, external_user_key
    .. pii_retirement: local_api
    """
    STATUSES = (
        ('enrolled', _('enrolled')),
        ('pending', _('pending')),
        ('suspended', _('suspended')),
        ('withdrawn', _('withdrawn')),
    )

    class Meta(object):
        app_label = "program_enrollments"

    user = models.ForeignKey(
        User,
        null=True,
        blank=True
    )
    email = models.EmailField(null=True, blank=True)
    external_user_key = models.CharField(
        db_index=True,
        max_length=255,
        null=True
    )
    program_uuid = models.UUIDField(db_index=True, null=False)
    curriculum_uuid = models.UUIDField(db_index=True, null=False)
    status = models.CharField(max_length=9, choices=STATUSES)
    historical_records = HistoricalRecords()

    @classmethod
    def retire_user(cls, user_id):
        """
        With the parameter user_id, retire the external_user_key and email fields

        Return True if there is data that was retired
        Return False if there is no matching data
        """

        enrollments = cls.objects.filter(user=user_id)
        if not enrollments:
            return False

        for enrollment in enrollments:
            enrollment.historical_records.update(email=None, external_user_key=None)

        enrollments.update(email=None, external_user_key=None)
        return True
