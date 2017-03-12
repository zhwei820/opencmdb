import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField

from functools import wraps
from django.utils.decorators import available_attrs
from django.http import JsonResponse

User = get_user_model()
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class VerificationBaseSerializer(object):
    """
    Abstract serializer used for verifying and refreshing JWTs.
    """

    def validate(self, attrs):
        msg = 'Please define a validate method.'
        raise NotImplementedError(msg)

    def _check_payload(self, token):
        # Check payload valid (based off of JSONWebTokenAuthentication,
        # may want to refactor)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)

        return payload

    def _check_user(self, payload):
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)

        # Make sure user exists
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)

        return user

class VerifyJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Check the veracity of an access token.
    """
    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)

        return {
            'token': token,
            'user': user
        }


# if __name__ == '__main__':
# a = VerifyJSONWebTokenSerializer()
# print(a.validate({"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmlnX2lhdCI6MTQ4NTA3NjcwOSwiZW1haWwiOiJ6d0AxLmNvbSIsInVzZXJuYW1lIjoienciLCJ1c2VyX2lkIjoxLCJleHAiOjE0ODUxMDY3MDl9.lJW59_E3dR-BjFhJ80BWJAieFzTqbnpc4b9jNzgJCzg"}))


def user_pass_func(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            user = test_func(request.META.get("HTTP_AUTHORIZATION"))
            if user:
                request.user = user
                return view_func(request, *args, **kwargs)
            result = {"status": "0", "message": "User not login"}
            return JsonResponse(result)
        return _wrapped_view
    return decorator


def verify(t):
    a = VerifyJSONWebTokenSerializer()
    try:
        res = a.validate({"token":t[3:].strip()})
        user = res['user']
    except Exception as e:
        return False
    else:
        return user

def login_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    
    actual_decorator = user_pass_func(verify)
    if function:
        return actual_decorator(function)
    return actual_decorator


from django.utils.deprecation import MiddlewareMixin

from api.models import UserActionLog
import json, datetime
from django.utils import timezone
class UserActionLoggingMiddleware(MiddlewareMixin):
    """
    This middleware log user every action  except GET
    
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(UserActionLoggingMiddleware, self).__init__(get_response=get_response)

    def process_request(self, request):
        if request.method != "GET" and request.path != "/api/api-token-auth/" and len(request.FILES) == 0:
            user = verify(request.META.get("HTTP_AUTHORIZATION"))
            if user:
                request.user = user

            request._body = request.read()

            user_action_log = UserActionLog()
            user_action_log.method = request.method
            user_action_log.content = request._body
            user_action_log.user_id = request.user.id
            user_action_log.user_name = request.user.username
            user_action_log.uri = request.path
            user_action_log.ctime = timezone.now()
            user_action_log.save()

        return None