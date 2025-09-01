from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

# Exception handler for requests
def register_exception_handler(app: FastAPI):
    """
    Registers exception handler for FastAPI

    """
    @app.add_exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(status_code = 500, content = {'detail': str(exc)})