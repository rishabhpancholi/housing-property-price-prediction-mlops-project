from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

# Register exception handlers function
def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "path": request.url.path
            }
        )