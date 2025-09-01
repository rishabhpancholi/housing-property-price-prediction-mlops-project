from fastapi import APIRouter
from app.model.schema import InputSchema
from app.services.model_service import get_prediction

# Creating an APIRouter instance
router = APIRouter()

# Creating a prediction route
@router.post("/predict")
async def predict(data: InputSchema)-> dict:
    """
    Returns predictions for the given data

    """
    prediction  = get_prediction(data.model_dump())
    return {"prediction": f'{prediction:,.2f}'} 



