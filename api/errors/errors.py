class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
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