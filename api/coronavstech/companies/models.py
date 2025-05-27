from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class CompanyStatus(models.TextChoices):
        LAYOFF = "Layoff"
        HIRING_FREEZE = "Hiring Freeze"
        HIRING = "Hiring"

    status = models.CharField(
        choices=CompanyStatus.choices, default=CompanyStatus.HIRING, max_length=30
    )
    last_update = models.DateTimeField(default=now, editable=True)
    application_link = models.URLField(max_length=100, blank=True)
    notes = models.TextField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
