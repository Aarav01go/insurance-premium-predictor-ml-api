from fastapi import FastAPI,Path,HTTPException,Query
#3 http exception custom error throw krta h fast api me ,,,, iski zarurat padi kyuki jb db me data nhi tha tabhi code 200 dera tha ie success
#path provide metadata,rules,validation and documentation hints for api
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='Patient ID')]
    name:Annotated[str,Field(...,description='Name')]
    city:Annotated[str,Field(...,description='City of living')]
    age:Annotated[int,Field(...)]
    gender:Annotated[Literal['male','female','other'],Field(default=None)]
    height:Annotated[float,Field(...,gt=0)]
    weight:Annotated[float,Field(...,gt=0)]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/self.height**2,2)

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'underweight'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'obese'
        
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(...,description='Name')]
    city:Annotated[Optional[str],Field(...,description='City of living')]
    age:Annotated[Optional[int],Field(...)]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height:Annotated[Optional[float],Field(...)]
    weight:Annotated[Optional[float],Field(...)]


def save_data(data):
    with open('patient.json','w')as f:
        json.dump(data,f)


def load_data():
    with open('patient.json','r')as f:
        data=json.load(f)
    return data


@app.get("/")
def hello():
    return {'message':'Patient management system API'}


@app.get("/about")
def about():
    return {'message':'An api to manage database of patient'}


@app.get('/view')
def view():
    data=load_data()
    return data


#{patient_id}hame help kar ra ki hm kisi specific PATIENt ko choose kr paye
@app.get('/patient/{patient_id}')

# 3 . ka mtlb h path parameter is required
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',examples=['P001'])):
    data=load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404,detail='Patient not found')


# jab bhi request ati jati h to http status code deta  h 3 digit ka these are of 4 types
# 2xx success
# 3xx redirection
# 4xx client error
# 5xx server error

# query params are optional , start with ?

@app.get('/sort')
def sort_parameter(sort_by:str=Query(...,description='sort by height , weight or bmi'),order:str=Query('asc',description='sort in ascending or descending order')):
    #yha p jb hamne query (...,) dala iska mtlb necessary h yani ki sort_by zaruri h
    #aur jo order h wo optional h kyuki 3 . nhi h ('asc') ka mtlb default ascending me sort karega
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'invalid field selected from {valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order selected')

    data=load_data()

    sort_order=True if order=='desc' else False
    #reverse true desc pe aur false pe asc

    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data


#[http://127.0.0.1:8000/sort?sort_by=height&order=desc](http://127.0.0.1:8000/sort?sort_by=height&order=desc) this was used to order optional


@app.post('/create')
#create patient p json me receive hoga and wo hm patient k roop m lenge aur fr pydantic object data validate krega
def create_patient(patient:Patient):
    #load existing data
    data=load_data()

    #check if patient exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient pehle se h')

    #agar nhi h to add kar denge in db
    #pydantic model ko dictionary me convert krenge and except id baaki data db me add hoga with a new code ie id, automatic bmi and verdict calc hoga bina diye
    data[patient.id]=patient.model_dump(exclude={'id'})

    #saving this dict into db by converting in json
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'pateint created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):#patient _update me ham dydantic model use karenge to check valid
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='PATIENT NHI HA RE BABA')
    
    existing_data=data[patient_id]
    
    # sabse pehle jo pydantic model load kiya  use dictionary banyenge kyu taaki ham compare kr paye extracted data and given ko
    
    Updated_patient_info=patient_update.model_dump(exclude_unset=True)
    # agar ham exclude unset true na kare to agar user ne sirf 2-3 cheeze di hongi fr bhi pura show karega true karne se only given one dikhayega
    
    for key,value in Updated_patient_info.items():
        existing_data[key]=value
    
    #existing info->pydantic obj->updated bmi+ verdict
    existing_data['id']=patient_id
    Patient_pydantic_obj=Patient(**existing_data)
    
    #pydantic obj->dict
    existing_data=Patient_pydantic_obj.model_dump(exclude='id')
    
   

    data[patient_id]=existing_data   
    
     # save data
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'pateint updated'})

@app.delete('/delete')
def delete_patient(patient_id:str):
    
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    