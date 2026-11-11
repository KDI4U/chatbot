from fastapi import HTTPException


class AppException(HTTPException):

    def __init__(
        self,
        status_code: int = 400,
        message: str = "Something went wrong."
    ):
        super().__init__(
            status_code=status_code,
            detail=message
        )   