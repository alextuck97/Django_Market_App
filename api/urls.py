from django.urls import path, include
from rest_auth import urls
from . import views

urlpatterns = [
    path('userportfolio/', views.RESTAccountPortfolio.as_view(), name="user-portfolio-control"),
    path('rest-auth/', include("rest_auth.urls"))
]