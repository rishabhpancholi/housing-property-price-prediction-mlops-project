from fastapi import APIRouter
from api.service import give_prediction
from api.model import load_model,HouseFeatures

# Load model
model = load_model()

# Prediction router
prediction_router = APIRouter()

# Prediction route
@prediction_router.post("/predict")
def predict(house_features: HouseFeatures)->dict:
    prediction = give_prediction(house_features,model)
    return {"predicted_house_price": prediction}