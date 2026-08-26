from pydantic import BaseModel, Field
from typing import Dict

class PredictResponce(BaseModel):
   predicted_category : str=Field(...,description='THE predicted insurance is of premium category',example='High')
   confidence: float = Field(...,description='Model confidence score for predicted class range from (0-1)',example=0.786)
   class_probabilities:Dict[str,float] = Field(...,description='Probability distribution across all possible classes',example={"Low":0.01,"Medium":0.15,"High":0.84})
   