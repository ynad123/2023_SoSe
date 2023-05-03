#main
#  python3 -m uvicorn main:app --reload --port 8000
from fastapi import FastAPI, Request
app = FastAPI()

persons = [{"last_name": "Mouse","first_name": "Micky","id": 1},
           {"last_name": "Mouse","first_name": "Minni","id": 2},
           {"last_name": "Donald","first_name": "Duck","id": 3}]

@app.get("/persons")
async def root_persons():
    return persons


@app.get("/persons/{id}")
async def read_person(id: int):
    #find correct person by id
    for p in persons:
        if p['id'] == id:
            return p
    return {}


@app.post("/persons")
async def newPerson(person: Request):
    new_person = await person.json()
    persons.append(new_person);
    
    return {
        "status" : "SUCCESS",
        "data" : new_person
    }
    
    
@app.delete("/persons/{id}")
async def deletePerson(id: int):
    for p in persons:
        if p['id'] == id:
            persons.remove(p)
            return {
                "status" : "SUCCESS"
            }
    return {}
