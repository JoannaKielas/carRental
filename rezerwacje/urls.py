from django.contrib import admin
from django.urls import path
from .views import AutoListView, reserve, unreserve, AutoDetailView, RezerwacjaListView

urlpatterns = [
    path('', AutoListView.as_view(), name="index"),
    path('rezerwacje', RezerwacjaListView.as_view(), name="rezerwacje"),
    path('reserve/<int:auto_id>', reserve, name="reserve"),
    path('unreserve/<int:rezerwacja_id>', unreserve, name="unreserve"),
    path('<int:pk>', AutoDetailView.as_view(), name="details")
]