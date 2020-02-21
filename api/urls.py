from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('watch/', views.ModifyWatchList.as_view(), name="account-transaction"),
    path('account-summary/', views.AccountInformation.as_view(), name="account-information"),
    path('token-auth/', obtain_jwt_token),
    path('create-user/', views.CreateUser.as_view(), name="create-user"),
    path('whoisthis/', views.CurrentUser().as_view(), name="get-current-user"),
    path('request-industry/<str:industry>/', views.RequestIndustry().as_view(), name="request-industry"),
    path('scrape-stock-data/<str:ticker>/<str:period>/<str:interval>/', views.RequestTicker().as_view(), name="request-ticker")
]