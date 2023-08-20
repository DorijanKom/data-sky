from celery import shared_task

from services.core.utils.token_manager import TokenManager


@shared_task
def delete_expired_tokens():
    TokenManager().delete_expired_tokens()


