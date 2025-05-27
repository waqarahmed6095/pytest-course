from rest_framework import routers
from api.coronavstech.companies.views import CompanyViewSet
from django.urls import path, include


companies_router = routers.DefaultRouter()
companies_router.register("companies", CompanyViewSet, basename="companies")
