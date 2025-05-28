import json
import os
from typing import List

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


@pytest.fixture()
def amazon() -> Company:
    return Company.objects.create(name="Amazon")


@pytest.fixture()
def companies(request, company) -> List[Company]:
    companies = []
    for company_name in request.param:
        companies.append(company(name=company_name))
    return companies


@pytest.fixture()
def company() -> callable:
    def _company_factory(**kwargs) -> Company:
        company_name = kwargs.pop("name", "Test Company INC")
        return Company.objects.create(name=company_name, **kwargs)

    return _company_factory


def test_zero_companies_should_return_empty_list(client) -> None:
    """
    Test that the API returns an empty list when there are no companies.
    """
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_should_return_one_company(client, amazon) -> None:
    """
    Test that the API returns a single company when there is one company.
    """
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content["name"] == amazon.name
    assert response_content["status"] == amazon.status
    assert response_content["application_link"] == amazon.application_link
    assert response_content["notes"] == amazon.notes


def test_create_company_without_args_should_fail(client) -> None:
    """
    Test that the API returns a 400 error when a company is created without arguments.
    """
    response = client.post(companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client) -> None:
    """
    Test that the API returns a 400 error when a company is created with the same name.
    """
    Company.objects.create(name="Amazon")
    response = client.post(companies_url, data={"name": "Amazon"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    """
    Test that the API returns a 201 error when a company is created with only a name.
    """
    response = client.post(companies_url, data={"name": "test company name"})
    assert response.status_code == 201
    assert Company.objects.count() == 1
    assert Company.objects.get().name == "test company name"
    assert Company.objects.get().status == "Hiring"
    assert Company.objects.get().application_link == ""
    assert Company.objects.get().notes == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    """
    Test that the API returns a 201 error when a company is created with the layoffs status.
    """
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
    """
    Test that the API returns a 400 error when a company is created with a wrong status.
    """
    response = client.post(
        companies_url,
        data={"name": "test company name", "status": "Wrong status"},
    )
    assert response.status_code == 400
    assert "Wrong status" in str(response.content)
    assert "is not a valid choice" in str(response.content)


@pytest.mark.parametrize(
    "companies",
    [["Twitch", "Tiktok", "Test Company INC"], ["Facebook", "Google", "Apple"]],
    indirect=True,
)
def test_multiple_companies_exists_should_succeed(client, companies) -> None:
    companies_names = set(map(lambda x: x.name, companies))
    reponse_companies = client.get(companies_url).json()
    assert len(companies_names) == len(reponse_companies)
    response_company_names = set(map(lambda x: x["name"], reponse_companies))
    assert response_company_names == set(companies_names)
