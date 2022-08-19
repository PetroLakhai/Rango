from django.urls import path

from rango import views

app_name = "rango"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path(
        "category/<slug:category_name_slug>/",
        views.ShowCategoryView.as_view(),
        name="show_category",
    ),
    path("add_category/", views.AddCategoryView.as_view(), name="add_category"),
    path(
        "category/<slug:category_name_slug>/add_page/",
        views.AddPageView.as_view(),
        name="add_page",
    ),
    path("restricted/", views.RestrictedView.as_view(), name="restricted"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("goto/", views.GoToUrlView.as_view(), name="goto"),
    path(
        "profile_registration/",
        views.ProfileRegistrationView.as_view(),
        name="profile_registration",
    ),
]
