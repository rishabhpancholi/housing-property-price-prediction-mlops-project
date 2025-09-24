from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import home_router,prediction_router
from api.exception import register_exception_handlers

# Initializing app
app = FastAPI(
    title="Housing Price Prediction API",
    description="""
An Application programming interface for a house price prediction model.

## Input
- Numerous house price features both categorical and numerical such as **num_bhk**, **location**, **carpet_area**, etc.

## Output
- The predicted value of house price in `crores` as a float value.
- The currency unit of the predicted house price is `rupees` (Indian).
""",
    version="1.0.0"
)

# Include routes
app.include_router(home_router)
app.include_router(prediction_router)

# Adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registering exception handlers
register_exception_handlers(app)

