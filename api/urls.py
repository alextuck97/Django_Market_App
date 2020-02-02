from django.urls import path, include
from rest_auth import urls
from . import views

urlpatterns = [
    path('transaction/', views.AccountTransactions.as_view(), name="account-transaction"),
    path('account-summary/', views.AccountInformation.as_view(), name="account-information"),
    path('rest-auth/', include("rest_auth.urls"))
]