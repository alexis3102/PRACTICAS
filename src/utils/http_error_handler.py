from fastapi import FastAPI, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

from typing import Awaitable, Callable

class HTTPErrorHandler(BaseHTTPMiddleware):
    def __init__(selft, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self,
                         request:Request,
                           call_next: Callable[[Request], Awaitable[JSONResponse]]
                           ) -> Response | JSONResponse:
        try:
            return await call_next(request)
            return Response
        except Exception as e:
            content = f"exc: {str(e)}"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return JSONResponse(
                content={"detail" :content},
                status_code=status_code
            )
            
