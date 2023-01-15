import pytest
from django.urls import reverse
from rango.models import Category


@pytest.mark.django_db
def test_index_view_with_no_categories(client) -> None:

    response = client.get(reverse('rango:index'))
    assert response.status_code == 200
    assert 'There are no categories present.' in str(response.content)


@pytest.mark.django_db
def test_index_view_with_categories(client) -> None:
    Category.objects.get_or_create(name='Python', views=1, likes=1)
    Category.objects.get_or_create(name='C++', views=1, likes=1)
    Category.objects.get_or_create(name='Erlang', views=1, likes=1)
    response = client.get(reverse('rango:index'))

    assert Category.objects.count() == 3
    assert response.status_code == 200
    assert 'Python' in str(response.content)
    assert 'C++' in str(response.content)
    assert 'Erlang' in str(response.content)


@pytest.mark.django_db
def test_about_page(client) -> None:
    response = client.get(reverse('rango:about'))

    assert response.status_code == 200


# @pytest.mark.django_db
# def test_restricted_page(client) -> None:
#     response = client.get(reverse('rango:restricted'))
#
#     assert response.status_code == 200















