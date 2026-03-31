from django.urls import include, path
from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("categories/", views.categories, name="categories"),
]