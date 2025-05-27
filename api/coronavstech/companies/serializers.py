from rest_framework import serializers

from api.coronavstech.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    A serializer for the Company model.
    """

    class Meta:
        """
        A class representing the metadata for the CompanySerializer.
        """

        model = Company
        fields = ["id", "name", "status", "application_link", "last_update", "notes"]
