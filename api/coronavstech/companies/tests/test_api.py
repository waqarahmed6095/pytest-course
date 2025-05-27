import json
import os

import django
import pytest
from django.urls import reverse

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "api.coronavstech.coronavstech.settings"
)
django.setup()

from api.coronavstech.companies.models import Company

pytestmark = pytest.mark.django_db

companies_url = reverse("companies-list")


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_should_return_one_company(client) -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content["name"] == test_company.name
    assert response_content["status"] == test_company.status
    assert response_content["application_link"] == test_company.application_link
    assert response_content["notes"] == test_company.notes


def test_create_company_without_args_should_fail(client) -> None:
    response = client.post(companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="Amazon")
    response = client.post(companies_url, data={"name": "Amazon"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(companies_url, data={"name": "test company name"})
    assert response.status_code == 201
    assert Company.objects.count() == 1
    assert Company.objects.get().name == "test company name"
    assert Company.objects.get().status == "Hiring"
    assert Company.objects.get().application_link == ""
    assert Company.objects.get().notes == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:

    response = client.post(
        companies_url, data={"name": "test company name", "status": "Layoff"}
    )
    assert response.status_code == 201
    assert Company.objects.count() == 1
    assert Company.objects.get().name == "test company name"
    assert Company.objects.get().status == "Layoff"
    assert Company.objects.get().application_link == ""
    assert Company.objects.get().notes == ""


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        companies_url,
        data={"name": "test company name", "status": "Wrong status"},
    )
    assert response.status_code == 400
    assert "Wrong status" in str(response.content)
    assert "is not a valid choice" in str(response.content)
