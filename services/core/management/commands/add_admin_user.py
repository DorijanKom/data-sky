import logging

from django.core.management.base import BaseCommand

from services.core.models import User

logger = logging.getLogger(__name__)

ADMIN_USER_EMAIL = "admin@sinbad.com"


class Command(BaseCommand):
    help = "Add admin user"

    def handle(self, *args, **options):
        if not User.objects.filter(email=ADMIN_USER_EMAIL).exists():
            user = User()
            user.email = ADMIN_USER_EMAIL
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            user.set_password("admin")
            user.save()
            logger.info("Admin user created...")
