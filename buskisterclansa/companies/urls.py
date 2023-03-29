# Django
from django.urls import path

# This app
from .views import CompanyView

app_name="companies"
urlpatterns = [
    path("<slug>/", CompanyView.as_view(), name="company_path"),
]
