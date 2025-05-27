from django.test import TestCase
from django.core import mail
from django.test import Client
import json
from unittest.mock import patch
class EmailUnittest(TestCase):
    def test_send_email_should_succeed(self)->None:
        with self.settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"):
            self.assertEqual(len(mail.outbox), 0)
            mail.send_mail(
                subject="Test Email",
                message="This is a test email",
                from_email="test@gmail.com",
                recipient_list=["test@gmail.com"],
            )
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, "Test Email")
            self.assertEqual(mail.outbox[0].body, "This is a test email")
            self.assertEqual(mail.outbox[0].from_email, "test@gmail.com")
            self.assertEqual(mail.outbox[0].to, ["test@gmail.com"])

    def test_send_email_without_arguments_should_send_empty_email(self)->None:
        client = Client()
        with patch("api.coronavstech.companies.views.send_mail") as mock_send_mail:
            response = client.post(path="/send-email/", data={})
            response_content = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_content["status"], "success")
            self.assertEqual(response_content["info"], "email sent successfully")
            mock_send_mail.assert_called_with(
                subject=None,
                message=None,
                from_email="waqarahmed695@gmail.com",
                recipient_list=["waqarahmed695@gmail.com"],
            )

    def test_send_email_with_get_verb_should_fail(self)->None:
        client = Client()
        response = client.get(path="/send-email/")
        self.assertEqual(response.status_code, 405)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["detail"], 'Method "GET" not allowed.')
