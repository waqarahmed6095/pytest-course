from unittest import TestCase
from django.test import Client
from django.urls import reverse
import json
import os
import django
import pytest

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "api.coronavstech.coronavstech.settings"
)
django.setup()

from api.coronavstech.companies.models import Company


@pytest.mark.django_db
class BasicCompanyAPITest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


@pytest.mark.django_db
class TestGetCompanies(BasicCompanyAPITest):

    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_should_return_one_company(self) -> None:
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content["name"], test_company.name)
        self.assertEqual(response_content["status"], test_company.status)
        self.assertEqual(
            response_content["application_link"], test_company.application_link
        )
        self.assertEqual(response_content["notes"], test_company.notes)
        test_company.delete()


class TestPostCompanies(BasicCompanyAPITest):
    def test_create_company_without_args_should_fail(self) -> None:
        response = self.client.post(self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="Amazon")
        response = self.client.post(self.companies_url, data={"name": "Amazon"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]},
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "test company name"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, "test company name")
        self.assertEqual(Company.objects.get().status, "Hiring")
        self.assertEqual(Company.objects.get().application_link, "")
        self.assertEqual(Company.objects.get().notes, "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "test company name", "status": "Layoff"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, "test company name")
        self.assertEqual(Company.objects.get().status, "Layoff")
        self.assertEqual(Company.objects.get().application_link, "")
        self.assertEqual(Company.objects.get().notes, "")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            self.companies_url,
            data={"name": "test company name", "status": "Wrong status"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Wrong status", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skipif
    def test_should_be_skipped(self) -> None:
        self.assertEqual(1, 1)


def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert str(e.value) == "CoronaVirus Exception"


import logging

logger = logging.getLogger("CORONA_LOGS")


def function_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
    assert "I am logging info level" in caplog.text
