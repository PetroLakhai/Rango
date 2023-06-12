import pytest

from rango.models import Category


@pytest.mark.django_db
def test_category_model() -> None:
    category, created = Category.objects.get_or_create(name="test", views=1, likes=0)

    assert created is True
    assert category.views == 1
    assert category.likes == 0
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_slug_line_creation() -> None:
    category, created = Category.objects.get_or_create(name="Random Category String")
    assert category.slug == "random-category-string"
