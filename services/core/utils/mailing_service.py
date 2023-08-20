import logging
import base64

import requests
from django.template import loader

from django.conf import settings

from config.settings.base import SITE_HOST
from services.core.utils.instance_loader import get_instance

logger = logging.getLogger(__name__)


class MailingService:
    def send(self, text_body, html_body, subject, from_email, to_email, **kwargs):
        logger.info("Send mail")
        logger.info(subject)
        logger.info(from_email)
        logger.info(to_email)
        logger.info(kwargs)
        files = []

        if "attachments" in kwargs and kwargs["attachments"]:
            for key, value in kwargs.get("attachments").items():
                files.append(
                    (
                        "attachment",
                        (
                            key.replace("\n", "").replace("\r", "").replace("\t", ""),
                            base64.b64decode(value.encode("utf-8")),
                        ),
                    )
                )

        if "files" in kwargs and kwargs["files"]:
            for key, value in kwargs.get("files").items():
                files.append(("attachment", value))

        payload = {"from": from_email, "to": to_email, "subject": subject, "text": text_body, "html": html_body}

        if "cc" in kwargs and kwargs["cc"]:
            payload["cc"] = kwargs.get("cc")

        if "bcc" in kwargs and kwargs["bcc"]:
            payload["bcc"] = kwargs.get("bcc")
        return self.make_request(payload, files)

    def send_to_address(self, to_email, template, subject="Sinbad", ctx=None):

        if ctx is None:
            ctx = {}

        if not ctx.get("site", False):
            site = {"name": "Sinbad", "domain": SITE_HOST}
            ctx["site"] = site

        text_body = "Textual email"
        html_body = loader.get_template("emails/{}.html".format(template)).render(ctx)

        if "to_email" in ctx:
            del ctx["to_email"]

        return self.send(text_body, html_body, subject, "sinbad@evolt.dev", to_email, **ctx)

    def make_request(self, payload, files):
        pass


class ExchangeMailService(MailingService):
    def make_request(self, payload, files):
        try:
            login_request = {
                "grant_type": "client_credentials",
                "client_id": settings.EXCHANGE_CLIENT_ID,
                "scope": "https://graph.microsoft.com/.default",
                "client_secret": settings.EXCHANGE_CLIENT_SECRET
            }
            login_request_url = "https://login.microsoftonline.com/29f0c17b-ba73-4ad8-a4a1-9128279ac059/oauth2/v2.0/token"
            login_response = requests.post(login_request_url, data=login_request)
            access_token = login_response.json()['access_token']

            send_mail_request = {
                "message": {
                    "subject": payload['subject'],
                    "body": {
                        "contentType": "html",
                        "content": payload['html']
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": payload['to']
                            }
                        }
                    ]
                },
                "saveToSentItems": "false"
            }

            send_mail_url = "https://graph.microsoft.com/v1.0/users/c3066c79-d412-46ae-af78-db8ec51223a7/sendMail"
            send_mail_headers = {"Authorization": "Bearer {}".format(access_token),
                                 "Content-Type": "application/json"}

            result = requests.post(send_mail_url, headers=send_mail_headers, data=str(send_mail_request))

            print(result)
            result.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            return False

        return True


class SmtpService(MailingService):
    def make_request(self, payload, files):
        from django.core import mail
        from django.core.mail import EmailMultiAlternatives

        connection = mail.get_connection()
        try:
            connection.open()
        except Exception as e:
            logger.exception(e)

        message = EmailMultiAlternatives(
            payload.get("subject"), payload.get("text"), payload.get("from"), [payload.get("to")], connection=connection
        )
        message.attach_alternative(payload.get("html"), "text/html")

        try:
            for file in files:
                message.attach(file[1][0], file[1][1])
        except Exception as e:
            logger.exception(e)

        try:
            message.send()
        except Exception as e:
            logger.exception(e)
            connection.close()
            return False

        connection.close()
        return True


def get_mail_service() -> MailingService:
    return get_instance(settings.MAIL_SERVICE_CLASS)
