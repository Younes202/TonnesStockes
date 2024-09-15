# exceptions.py

from fastapi import HTTPException, status


class AdminSignupForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin users are not authorized to sign up."
        )


class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists. Please try with another email."
        )


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
