from rest_framework import status
from services.core.utils.error import Error

GLOBAL_VALIDATION_ERROR = "notValid"
WRONG_CREDENTIALS = "wrongCredentials"
TOKEN_MISSING = "tokenMissing"
DIRECTORY_ALREADY_EXISTS = "directoryAlreadyExists"
FILE_ALREADY_EXISTS = "fileAlreadyExists"

ERROR_OBJECTS = {
    GLOBAL_VALIDATION_ERROR: (
        Error(GLOBAL_VALIDATION_ERROR, "Validation failed"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    WRONG_CREDENTIALS: (
        Error(WRONG_CREDENTIALS, "Wrong credentials"),
        status.HTTP_400_BAD_REQUEST,
    ),
    TOKEN_MISSING: (
        Error(TOKEN_MISSING, "Token missing"),
        status.HTTP_403_FORBIDDEN
    ),
    DIRECTORY_ALREADY_EXISTS: (
        Error(DIRECTORY_ALREADY_EXISTS, "Directory already exists"),
        status.HTTP_400_BAD_REQUEST
    ),
    FILE_ALREADY_EXISTS: (
        Error(FILE_ALREADY_EXISTS, "File with that name already exists"),
        status.HTTP_400_BAD_REQUEST
    )
}

