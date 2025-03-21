from enum import Enum


class ErrorCode(str, Enum):
    PROJECT_ALREADY_EXISTED = "4000001"
    NOT_FOUND_SUCH_ITEM = "40432000"
    NO_PERMISSION = "40332000"

    UNAUTHORIZED_PASSPORT = "40132000"
    UNAUTHENTICATED_PASSPORT = "40132001"

    INTERNAL_SERVER_ERROR = "50032000"


ERROR_MESSAGES = {
    ErrorCode.NOT_FOUND_SUCH_ITEM.value: "Not found such item",
    ErrorCode.NO_PERMISSION.value: "No permission",
    ErrorCode.UNAUTHORIZED_PASSPORT.value: "Invalid authentication credentials",
    ErrorCode.UNAUTHENTICATED_PASSPORT.value: "Unauthenticated credentials with passport",
}
