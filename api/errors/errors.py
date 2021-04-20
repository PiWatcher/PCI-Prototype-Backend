class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class FailedEntryCreationError(Exception):
    pass

class FailedRoleCreationError(Exception):
    pass

class FailedRoleDeletionError(Exception):
    pass

class FailedUserCreationError(Exception):
    pass

class FailedUserDeletionError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class EmailDoesNotExistError(Exception):
    pass

class RoleAlreadyExistsError(Exception):
    pass

class RoleDoesNotExistError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class BadTokenError(Exception):
    pass

errors = {
    "InternalServerError": {
        "status": 500,
        "message": "Something went wrong. Please contact your system administrator."
    },
    "SchemaValidationError": {
        "status": 400,
        "message": "Request is missing required fields."
    },
    "FailedEntryCreationError": {
        "status": 400,
        "message": "Entry failed to create. Try again."
    },
    "FailedRoleCreationError": {
        "status": 400,
        "message": "Role failed to create. Try again."
    },
    "FailerRoleDeleteError": {
        "status": 400,
        "message": "Role failed to delete. Try again."
    },
    "FailedUserCreationError": {
        "status": 400,
        "message": "User failed to create. Try again."
    },
    "FailedUserDeletionError": {
        "status": 400,
        "message": "User failed to delete. Try again."
    },
    "EmailAlreadyExistsError": {
        "status": 400,
        "message": "An account with that given email address already exists."
    },
    "EmailDoesNotExistError": {
        "status": 400,
        "message": "Couldn't find the user with given email address."
    },
    "RoleAlreadyExistsError": {
        "status": 400,
        "message": "That role has already been created."
    },
    "RoleDoesNotExistError": {
        "status": 400,
        "message": "That role does not exist."
    },
    "UnauthorizedError": {
        "status": 401,
        "message": "Invalid username or password."
    },
    "BadTokenError": {
        "status": 403,
        "message": "Invalid token."
    }
}