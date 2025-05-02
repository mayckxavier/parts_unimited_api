from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class DatabaseError(Exception):
    def __init__(self, detail: str = "Database error occurred"):
        self.detail = detail


def add_exception_handlers(app: FastAPI) -> None:
    """
    Add exception handlers to the FastAPI application
    """

    @app.exception_handler(DatabaseError)
    async def db_exception_handler(request: Request, exc: DatabaseError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": exc.detail},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred"},
        )
