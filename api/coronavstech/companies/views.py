"""
Views for the Company model.
"""

from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from api.coronavstech.companies.models import Company
from api.coronavstech.companies.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for the Company model.
    """

    queryset = Company.objects.all().order_by("-last_update")
    serializer_class = CompanySerializer
    pagination_class = PageNumberPagination


@api_view(http_method_names=["POST"])
def send_company_email(request: Request):
    """
    Send email with request payload.
    """
    send_mail(
        subject=request.data.get("subject"),
        message=request.data.get("message"),
        from_email="waqarahmed695@gmail.com",
        recipient_list=["waqarahmed695@gmail.com"],
    )

    return Response(
        {"status": "success", "info": "email sent successfully"}, status=200
    )
