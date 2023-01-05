import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_authorization(client) -> None:
   url = 'http://127.0.0.1:8000/accounts/login/'
   response = client.get(url)
   assert response.status_code == 200


@pytest.mark.django_db
def test_superuser_view(admin_client) -> None:
   url = "http://127.0.0.1:8000/admin/"
   response = admin_client.get(url)
   assert response.status_code == 200


@pytest.mark.django_db
def test_unauthorized(client) -> None:
   url = "http://127.0.0.1:8000/admin/"
   response = client.get(url)
   assert response.status_code == 302



