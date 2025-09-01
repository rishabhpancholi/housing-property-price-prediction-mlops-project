from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from api.routes.routes_predict import predict_router
from api.routes.routes_home import home_router
from api.core.exceptions import register_exception_handler
from api.middleware.logging_middleware import LoggingMiddleware

# Creating a FastAPI application
app = FastAPI(
        title = "Housing Property Price Prediction API", 
        description = "API to predict the price of a house given its features", 
        version = "0.1.0"
)

# Registering exception handlers
register_exception_handler(app)

# Including middleware
app.add_middleware(LoggingMiddleware)

# Including routes
app.include_router(home_router, tags = ["Home"])
app.include_router(predict_router, tags = ["Prediction"])

# Monitor the application using Prometheus
Instrumentator().instrument(app).expose(app)
