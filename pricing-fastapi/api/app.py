import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile, Request
from joblib import dump, load
import json

### 
# configurations 
###

description="""You can use this API to estimate the rental price of a car.
The API is based on a dataset of cars from Getaround.
## Who is GetAround ? 
### Main highlights are:

- `Top 2 player` : globally in peer-to-peer carsharing 
− `Operates` : in 950 cities across 8 countries, with 1.6m guests renting 66k cars from hosts Large total addressable market enabled by digital model
− Serviceable addressable market of $155B Proven path to profitability 
− Proven `profitability per transaction` : >50% trip contribution margin
− Proven `profitability per city` : Top 20 cities in aggregate are EBITDA positive Fully funded business plan and highly attractive financial profile
− Projected EBITDA breakeven with transaction proceeds Marketplace model is asset-light and powered by network effects
− Strong `long-term defensibility` of carsharing model Differentiated tech of connected cars enables superior UX
− Creates `uniquely seamless` host and renter value

In this project, we are looking for price optimization for rental price per day !
- `rental_price_per_day`: the rental price of the car (in $)

## Sample rows
* `/`: **GET** request that display random examples of the data.

## Search model
* `/search_model_key/{model_key}`: **GET** request that retrieve data for a car model

## Machine Learning 

This machine learning endpoint predict the optimum rental price per day given your car features.

Endpoints:

* `/predict`

Check out documentation below 👇 for more information on each endpoint.
"""


tags_metadata = [
    {
        "name": "Sample rows",
        "description": "Simple endpoints to try out!",
    },

    {
        "name": "Search model",
        "description": "Search data for a type of car model"
    },

    {
        "name": "Machine Learning",
        "description": "Prediction Endpoint."
    }
]


app = FastAPI(
    title="Getaround Pricing Predictor API",
    description=description,
    version="0.1",
    contact={
        "name": "Basma FEZZI",
        "url": "https://github.com/fezzibasma",
    },
    openapi_tags=tags_metadata
)


###
# endpoints 
###


@app.get("/")
async def index():
    message = """Welcome to the GetAround API ! This app is made to give you the optimum price at which you should rent your car on the GetAround app.The model used for prediction is a Extreme Gradient Boost trained from data collected by the GetAround data scientits team."""
    return message


@app.get("/", tags=["Sample cars"])
async def load_sample_cars():
    """
    display some (5) random examples of the data
    """

    cars = pd.read_csv("get_around_pricing_project.csv", index_col=0)

    car = cars.sample(5)

    return car.to_dict("index")


@app.get("/Search_model_key/{model_key}", tags=["Search model"])
async def search_model_key(model_key: object):
    """
    Search data by model key :
    Citroën, Peugeot, PGO, Renault, Audi, BMW, Ford,
    Mercedes, Opel, Porsche, Volkswagen, KIA Motors,
    Alfa Romeo, Ferrari, Fiat, Lamborghini, Maserati,
    Lexus, Honda, Mazda, Mini, Mitsubishi, Nissan, SEAT,
    Subaru, Suzuki, Toyota, Yamaha
   
    """

    cars = pd.read_csv("get_around_pricing_project.csv", index_col=0)

    rental_model = cars[cars["model_key"]==model_key]

    return rental_model.to_dict("index")

# endpoint to predict the price of a car

# Defining required input for the prediction endpoint
class PredictionFeatures(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool
    
@app.post("/predict", tags=["Machine Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Get the predicted price of a car. 
    You must fill in : 

{
  "model_key": Citroën Peugeot, PGO, Renault, Audi, BMW, Ford, Mercedes...
  
  "mileage": enter numerical value
  
  "engine_power": enter numerical value
  
  "fuel": petrol, hybrid_petrol, electro
  
  "paint_color": black, grey, white, red, silver, blue, orange, beige, brown, green
  
  "car_type": convertible, coupe, estate, hatchback, sedan, subcompact, suv, van
  
  "private_parking_available": True,False
  
  "has_gps": True,False
  
  "has_air_conditioning": True,False
  
  "automatic_car": True,False
  
  "has_getaround_connect": True,False
  
  "has_speed_regulator": True,False
  
  "winter_tires": True 
}

All entries are case sensitive.

Return a dict like this : {'predictions' : rental_price_per_day}


Wrong values will return a specific error message.
    """
    
    # Read data 
    data = pd.DataFrame(dict(predictionFeatures), index=[0])
    # Load model
    loaded_model = load('model_xg.joblib')
    #Prediction
    prediction = loaded_model.predict(data)
    #Load response
    response ={"predictions": prediction.tolist()[0]}
    return response

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 4000, debug=True, reload=True)
