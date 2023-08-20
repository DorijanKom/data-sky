import datetime

from rest_framework.authentication import get_authorization_header
import pytz

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions

from services.core.models.token import CustomToken


class CustomAuthentication:

    model = None
    keyword = 'Token'

    def get_model(self):
        if self.model is not None:
            return self.model
        return CustomToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        utc = pytz.UTC

        current_datetime = utc.localize(datetime.datetime.now())

        if token.valid_until < current_datetime:
            raise exceptions.AuthenticationFailed(_('Token has expired.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token

    def authenticate_header(self, request):
        return self.keyword

