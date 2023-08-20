import json
import logging
import traceback

from django.conf import settings
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    MethodNotAllowed,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

from services.core.constants.error import ERROR_OBJECTS
from services.core.serializers.error import ErrorSerializer
from services.core.utils.error import Error
from services.core.utils.wrapper_exception import WrapperException

DEFAULT_ERROR = Error("globalError", "Error was not processed validly! Please check logs for more details")
ERROR_TYPES_BLACKLIST = [
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    MethodNotAllowed,
    serializers.ValidationError,
]
logger = logging.getLogger(__name__)


def camelCase(s):
    return s[:1].lower() + s[1:] if s else ""


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        status_code = 500
    else:
        status_code = response.status_code

    if exc is not None and settings.LOG_ERROR_TRACE and type(exc) not in ERROR_TYPES_BLACKLIST:
        t = traceback.format_exc()
        logger.error(t)

    exc1 = exc
    inner_exceptions = []
    i = 0
    while exc1.__context__ is not None:
        exc1 = exc1.__context__
        inner_exceptions.append({"error": type(exc1).__name__, "reason": str(exc1)})
        i += 1
        if i > 2:
            break

    if isinstance(exc, ValidationError):
        logger.error("Exception handler: {}".format(str(exc)))

        grouped_err = filter_messages(exc.get_full_details().items())
        reason = []
        for x in grouped_err:
            reason.append({"fields": grouped_err[x], "reason": x})
        return Response(
            ErrorSerializer(Error("validationError", json.dumps(reason), stack=inner_exceptions)).data, status_code
        )
    elif isinstance(exc, WrapperException):
        if exc.status_code:
            status_code = exc.status_code
        error_response = __get_error_from_code(exc.error, status_code, exc.reason, inner_exceptions)

        logger.error(exc)
        logger.error("Exception handler: {}".format(error_response))
        if error_response is None:
            if exc.reason is None and settings.DEBUG:
                return Response(
                    ErrorSerializer(Error("assertionError", "%s error object is missing" % exc.error)).data, status_code
                )
            return Response(ErrorSerializer(Error(exc.error, exc.reason, stack=exc.stack)).data, status_code)
        error_response.errors = inner_exceptions
        return error_response

    if settings.LOG_EXCEPTION:
        logger.error("Exception handler: {}".format(str(exc)))

    return Response(ErrorSerializer(Error(camelCase(type(exc).__name__), str(exc))).data, status_code)


def error_response_from_code(error, status_code=None, reason=None):
    error_response = __get_error_from_code(error, status_code, reason)
    if error_response is not None:
        logger.error("Exception handler: {}".format(error))
        return error_response
    if settings.DEBUG:
        raise AssertionError("%s error object is missing" % error)

    response_data = ErrorSerializer(DEFAULT_ERROR).data

    logger.error("Exception handler: {}".format(str(response_data)))
    return Response(response_data, status_code)


def __get_error_from_code(error, status_code, reason, errors=None):
    if error in ERROR_OBJECTS:
        e = ERROR_OBJECTS.get(error)
        error_obj = e[0]
        if status_code is None:
            status_code = e[1]
        if reason is not None:
            error_obj.message = reason
            error_obj.reason = reason
        if errors is not None:
            error_obj.errors = errors
        return JsonResponse(ErrorSerializer(error_obj).data, status=status_code)
    return None


def filter_messages(items, base_field=None):
    grouped_err = {}

    if isinstance(items, dict):
        items = items.items()

    for field, details in items:
        if isinstance(details, dict):
            sub_groups = filter_messages(details.items(), format_field_name(base_field, field))
            for detail, sub_group_names in sub_groups.items():
                for sub_group in sub_group_names:
                    add_err_message(grouped_err, detail, sub_group)
        elif isinstance(details, list):
            sub_groups = {}
            for idx, detail in enumerate(details):
                if "message" in detail:
                    detail = detail["message"].capitalize()
                    add_err_message(grouped_err, detail, format_field_name(base_field, field))
                else:
                    sub_groups = filter_messages(detail, format_field_name(base_field, field, idx))
                    for detail, sub_group_names in sub_groups.items():
                        for sub_group in sub_group_names:
                            add_err_message(grouped_err, detail, sub_group)

    return grouped_err


def add_err_message(grouped_err, key, value):
    if key in grouped_err:
        grouped_err[key].append(value)
    else:
        grouped_err[key] = [value]


def format_field_name(base_field, field, index=None):
    if base_field:
        return "{}.{}".format(base_field, field)
    elif index is not None:
        return "{}.{}".format(field, index)
    else:
        return field
