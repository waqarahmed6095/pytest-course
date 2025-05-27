from django.core import mail
import json
from unittest.mock import patch



def test_send_email_should_succeed(mailoutbox, settings) -> None:

    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    mail.send_mail(
        subject="Test Email",
        message="This is a test email",
        from_email="test@gmail.com",
        recipient_list=["test@gmail.com"],
    )
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Test Email"
    assert mailoutbox[0].body == "This is a test email"
    assert mailoutbox[0].from_email == "test@gmail.com"
    assert mailoutbox[0].to == ["test@gmail.com"]


def test_send_email_without_arguments_should_send_empty_email(client) -> None:
    with patch("api.coronavstech.companies.views.send_mail") as mock_send_mail:
        response = client.post(path="/send-email/", data={})
        response_content = json.loads(response.content)
        assert response.status_code == 200
        assert response_content["status"] == "success"
        assert response_content["info"] == "email sent successfully"
        mock_send_mail.assert_called_with(
            subject=None,
            message=None,
            from_email="waqarahmed695@gmail.com",
            recipient_list=["waqarahmed695@gmail.com"],
        )


def test_send_email_with_get_verb_should_fail(client) -> None:
    response = client.get(path="/send-email/")
    assert response.status_code == 405
    response_content = json.loads(response.content)
    assert response_content["detail"] == 'Method "GET" not allowed.'
