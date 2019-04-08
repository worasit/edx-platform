"""
Unit tests for ProgramEnrollment models.
"""
from __future__ import unicode_literals

from uuid import uuid4

from django.test import TestCase

from lms.djangoapps.program_enrollments.models import ProgramEnrollment, User
from student.tests.factories import UserFactory


class ProgramEnrollmentModelTests(TestCase):
    """
    Tests for the ProgramEnrollment model.
    """
    def setUp(self):
        """
        Set up the test data used in the specific tests
        """
        super(ProgramEnrollmentModelTests, self).setUp()
        UserFactory.create()
        self.user = User.objects.first()
        self.email = 'foo@bar.com'
        self.external_user_key = 'abc'
        self.program_uuid = uuid4()
        self.curriculum_uuid = uuid4()
        self.status = 'enrolled'

        ProgramEnrollment.objects.create(
            user=self.user,
            email=self.email,
            external_user_key=self.external_user_key,
            program_uuid=self.program_uuid,
            curriculum_uuid=self.curriculum_uuid,
            status=self.status
        )

        self.enrollment = ProgramEnrollment.objects.first()


    def test_user_retirement(self):
        """
        Test that the email address and external_user_key are
        successfully retired for a user's program enrollments and history.
        """
        newStatus = 'withdrawn'

        self.enrollment.status = newStatus
        self.enrollment.save()

        # Ensure that all the records had values for email and external_user_key
        self.assertEquals(self.enrollment.email, 'foo@bar.com')
        self.assertEquals(self.enrollment.external_user_key, 'abc')

        for record in self.enrollment.historical_records.all():
            self.assertEquals(record.email, 'foo@bar.com')
            self.assertEquals(record.external_user_key, 'abc')

        ProgramEnrollment.retire_user(self.user.id)

        # Ensure those values are retired
        self.assertEquals(self.enrollment.email, 'foo@bar.com')
        self.assertEquals(self.enrollment.external_user_key, 'abc')

        for record in self.enrollment.historical_records.all():
            self.assertEquals(record.email, None)
            self.assertEquals(record.external_user_key, None)
