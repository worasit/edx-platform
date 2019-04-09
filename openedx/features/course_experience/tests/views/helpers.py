"""
Test helpers for the course experience.
"""
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from course_modes.models import CourseMode

TEST_COURSE_PRICE = 50


def add_course_mode(course, mode_slug, mode_display_name, upgrade_deadline_expired=False):
    """
    Adds a course mode to the test course.
    """
    upgrade_exp_date = now()
    if upgrade_deadline_expired:
        upgrade_exp_date = upgrade_exp_date - timedelta(days=21)
    else:
        upgrade_exp_date = upgrade_exp_date + timedelta(days=21)

    CourseMode(
        course_id=course.id,
        mode_slug=mode_slug,
        mode_display_name=mode_display_name,
        min_price=TEST_COURSE_PRICE,
        _expiration_datetime=upgrade_exp_date,
    ).save()

def remove_course_mode(course, mode_slug):
    try:
        mode = CourseMode.objects.get(course_id=course.id, mode_slug=mode_slug)
    except ObjectDoesNotExist:
        pass

    mode.delete()
