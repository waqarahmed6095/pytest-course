from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from api.coronavstech.companies.models import Company
from api.coronavstech.companies.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by("-last_update")
    serializer_class = CompanySerializer
    pagination_class = PageNumberPagination
