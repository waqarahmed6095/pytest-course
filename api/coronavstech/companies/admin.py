"""
Admin for the Company model.
"""

from django.contrib import admin

from api.coronavstech.companies.models import Company


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Admin for the Company model.
    """

    pass
