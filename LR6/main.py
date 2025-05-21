from http.client import HTTPException
from typing import Union
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select



app = FastAPI()

class Term(BaseModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(default='error')

glossary: dict[str,Term]={
    'REST': Term(
        name="REST",
        description = 'передача репрезентативного состояния'),
    'RPC': Term(
        name="RPC",
        description = 'Удаленный вызов процедур')
}

engine = None
engine = create_engine('mysql+pymysql://jama:8888@db/lr6')
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

print(engine)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/dbconnect')
def get_db_info():
    return str(engine)

@app.get("terms/{term}")
def get_term(term:str):
    if term not in glossary:
        raise HTTPException(status_code=404, detail = "Term not found")
    return glossary.get(term,"term not found")

@app.post("terms/{term}",response_model=dict[str,Term])
def post_term(term: str, term_data: Term):
    if term in glossary: # Corrected condition
        raise HTTPException(status_code=400, detail="Term already exists!")
    glossary[term] = term_data
    return {term: term_data}

@app.put("terms/{term}",response_model=dict[str,Term])
def change_term(term:str,term_data:Term):
    if term not in glossary:
        raise HTTPException(status_code=400, detail = "Term not found!")
    glossary[term] = term_data
    return {term: term_data}

@app.delete("terms/{term}")
def del_term(term:str):
    if term not in glossary:
        raise HTTPException(status_code=404, detail = "Term not found!")
    del glossary[term]
    return {"result":"deleted successfully"}

@app.get("/terms")
def all_get_term():
    return glossary

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
#
# @app.get("/author")
# def read():
#     current_datetime = datetime.now().strftime("%A, %m/%d/%Y")
#     return {"author": "Lera", "datetime": current_datetime}
#
# @app.get("/valute/{valute_id}")
# def read_valute(valute_id: str, _valute: Valute):
#     return {"valute_id": valute_id, "name": _valute.name, "value": _valute.value}
#
# @app.put(f"/items/{valute_id}")
# def update_item(valute_id: str, value: Value):
#     return {"valute_name": _valute.name, "valute_id": valute_id}
