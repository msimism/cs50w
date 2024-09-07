from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("random/", views.random_page, name="random"),
    path('new/', views.new_page, name='new_page'), 
]
