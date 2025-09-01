from fastapi import APIRouter
from api.model.schema import InputSchema
from api.services.model_service import get_prediction

# Creating an APIRouter instance
predict_router = APIRouter()

# Creating a prediction route
@predict_router.post("/predict")
async def predict(data: InputSchema)-> dict:
    """
    Returns predictions for the given data

    """
    prediction  = await get_prediction(data.model_dump())
    return {"prediction in crores": f'{prediction:,.2f}'} 



