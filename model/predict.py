import pickle
import pandas as pd
import os

#importing ml model 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'model.pkl'), 'rb') as f:
    model = pickle.load(f)
    
#ml flow se model version banayenge lekin abhi manually kr re h

MODEL_Version='1.0.0'

# get class label from model(important for matching probabilities to class name)
class_label = model.classes_.tolist()

def predict_output(user_input:dict):
   input_df= pd.DataFrame([user_input])
   
   output=model.predict(input_df)[0]
   
   
   
   #get probabilities for all classes
   probabilities=model.predict_proba(input_df)[0]
   confidence = max(probabilities)
   
   #create mapping:{class_name:probability}
   class_prob= dict(zip(class_label,map(lambda p:round(p,4),probabilities)))
   
   
   return {
      "predicted_category":output,
      "confidence": round(confidence,4),
      "class_probability": class_prob
   }