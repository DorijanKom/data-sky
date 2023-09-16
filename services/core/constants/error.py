from rest_framework import status
from services.core.utils.error import Error

GLOBAL_VALIDATION_ERROR = "notValid"
WRONG_CREDENTIALS = "wrongCredentials"
TOKEN_MISSING = "tokenMissing"
DIRECTORY_ALREADY_EXISTS = "directoryAlreadyExists"
DIRECTORY_DOES_NOT_BELONG_TO_USER = "directoryDoesNotBelongToUser"
FILE_ALREADY_EXISTS = "fileAlreadyExists"
FILE_DOES_NOT_EXIST = 'fileDoesNotExist'

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
    ),
    FILE_DOES_NOT_EXIST: (
        Error(FILE_DOES_NOT_EXIST, "The given file does not exist"),
        status.HTTP_404_NOT_FOUND
    ),
    DIRECTORY_DOES_NOT_BELONG_TO_USER: (
        Error(DIRECTORY_DOES_NOT_BELONG_TO_USER, "The parent directory does not belong to this user"),
        status.HTTP_403_FORBIDDEN
    )
}

