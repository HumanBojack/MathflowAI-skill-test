from django.urls import path
from . import views

urlpatterns = [
    path("random/", views.get_random_question, name="get-random-question"),
    path("money/<int:user_id>", views.get_money_buffer, name="get-money-buffer"),
]
