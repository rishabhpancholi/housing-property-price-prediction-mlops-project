from fastapi import APIRouter

# Home router
home_router = APIRouter()

# Home route
@home_router.get("/")
def home()->dict:
    return {"message": "Welcome to the House Price Prediction API"}

