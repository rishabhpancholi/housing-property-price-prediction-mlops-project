from fastapi import APIRouter

# Creating an APIRouter instance
home_router = APIRouter()

# Creating a prediction route
@home_router.get("/")
def home()-> dict:
    """
    Returns welcome message for the API

    """
    return {"message" : "Welcome to the Housing Property Price Prediction API"}