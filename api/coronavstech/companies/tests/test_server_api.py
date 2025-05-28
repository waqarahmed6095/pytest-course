import json

import requests

TEST_ENV_COMPANIES_URL = "http://localhost:8000/companies/"


def test_zero_companies_django_agnostic() -> None:
    """
    Test that the API returns an empty list when there are no companies.
    """
    response = requests.get(TEST_ENV_COMPANIES_URL, timeout=10)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_create_company_with_layoffs_django_agnostic() -> None:
    """
    Test that the API returns a 201 error when a company is created with the layoffs status.
    """
    response = requests.post(
        TEST_ENV_COMPANIES_URL,
        data={"name": "test company name", "status": "Layoff"},
        timeout=10,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test company name"
    assert response.json()["status"] == "Layoff"
    assert response.json()["application_link"] == ""
    assert response.json()["notes"] == ""
    cleanup_company(response.json()["id"])


def cleanup_company(company_id: int) -> None:
    response = requests.delete(
        TEST_ENV_COMPANIES_URL + str(company_id) + "/", timeout=10
    )
    assert response.status_code == 204
