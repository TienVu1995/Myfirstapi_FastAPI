# Import
import fastapi
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel



app=FastAPI()

students={
    1:{
        "name":"john",
        "age":17,
        "year":"Year 12"
    }
}


class Student(BaseModel):
    name:str
    age:int
    year:str

class UpdateStudent(BaseModel):
    name:Optional[str]=None
    age:Optional[int]=None
    year:Optional[str]=None

# Get method
@app.get("/")
def index():
    return{"name":"First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id:int=Path(...,description="input the Id of the student",gt=0,lt=3)):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*,student_id:int,name:Optional[str]=None, test:Optional[int]=None):
    for student_id in students:
        if students[student_id]['name']==name:
            return students[student_id]
    return {"Data":"Not found"} 

# Post method
@app.post("/create-student/{student_id}")
def create_student(student_id:int,body:Student):
    if student_id in students:
        return {"Error":"Student exist"}
    students[student_id]=body 
    return students[student_id]

# Put method (with partial update)
@app.put("/update-student/{student_id}")
def update_student(student_id: int, update_data: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    student = students[student_id]

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(student, field, value)

    return student

# Delete method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return {"Error":"Student does not exist"}
    
    del students[student_id]
    return {"Message":"Deleted Successfully"}