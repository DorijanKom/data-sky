from celery import shared_task
from django.conf import settings


@shared_task
def test_1():
    print("################# TEST 1 #######################")

