from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sklearn
from schema.user_input import UserInput
from model.predict import predict_output,model,MODEL_Version
from schema.prediction_responce import PredictResponce


app=FastAPI()

@app.get('/')
def home():
   return {'message':'INSURANCE PREMIUM PREDICTOR API'}


   
@app.get('/health')
def health_check():
   return{
      'status':'OK',
      'version':MODEL_Version 
   }




@app.post('/predict',response_model=PredictResponce)
def predict_premium(data: UserInput):
   
   user_input= pd.DataFrame([{
      'bmi':data.bmi,
      'age_group':data.age_group,
      'lifestyle_risk':data.lifestyle_risk,
      'city_tier':data.city_tier,
      'income_lpa':data.income_lpa,
      'occupation':data.occupation
   }])
   
   
   prediction= predict_output(user_input)
   
   return JSONResponse(status_code=200,content={'predict_category':str(prediction)})