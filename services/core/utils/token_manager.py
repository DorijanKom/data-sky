import datetime

from services.core.models.token import CustomToken


class TokenManager:

    def delete_expired_tokens(self):
        return CustomToken.objects.filter(valid_until__lt=datetime.datetime.now()).delete()
