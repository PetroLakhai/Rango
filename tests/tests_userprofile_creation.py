import pytest
from django.contrib.auth.models import User

from rango.models import UserProfile


@pytest.mark.django_db
def test_userprofile_created_with_user(client) -> None:
    """ """
    User.objects.get_or_create(username="dvdvf", id=19)

    assert UserProfile.objects.count() == 1
    assert User.objects.count() == 1
