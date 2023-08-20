from rest_framework import status
from services.core.utils.error import Error

GLOBAL_VALIDATION_ERROR = "notValid"
INSUFFICIENT_FUNDS_ERROR = "noFunds"

ERROR_OBJECTS = {
    GLOBAL_VALIDATION_ERROR: (
        Error(GLOBAL_VALIDATION_ERROR, "Validation failed"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    INSUFFICIENT_FUNDS_ERROR: (
        Error(INSUFFICIENT_FUNDS_ERROR, "Not enough funds"),
        status.HTTP_400_BAD_REQUEST,
    ),

}

