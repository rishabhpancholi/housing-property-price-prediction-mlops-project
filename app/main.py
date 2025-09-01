from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routes_predict import predict_router
from app.core.exceptions import register_exception_handlers
from app.middleware.logging_middleware import LoggingMiddleware

# Creating a FastAPI application
app = FastAPI(
        title = "Housing Property Price Prediction API", 
        description = "API to predict the price of a house given its features", 
        version = "0.1.0"
)

# Registering exception handlers
register_exception_handlers(app)

# Including middleware
app.add_middleware(LoggingMiddleware)

# Including routes
app.include_router(predict_router, tags = ["Prediction"])

# Monitor the application using Prometheus
Instrumentator().instrument(app).expose(app)
