#main
#  start local e.g.: python3 -m uvicorn main:app --reload --port 8000
from fastapi import FastAPI, Request
app = FastAPI()

werte = [{"tstamp": "2023-02-17 14:48:00","value": 42,"id": 1},
           {"tstamp": "2023-02-17 14:49:00","value": 34,"id": 2},
           {"tstamp": "2023-02-17 14:50:00","value": 17,"id": 3}]

@app.get("/werte")
async def root_werte():
    return werte

@app.get("/werte/latest")
async def read_werte_latest():
    #fget the last values
    l = len(werte)
    if l>0:
        return werte[l-1]
    else:
        return {}
    

@app.get("/werte/{id}")
async def read_werte(id: int):
    #find correct person by id
    for w in werte:
        if w['id'] == id:
            return w
    return {}

    
@app.post("/werte")
async def newWert(wert: Request):
    new_wert = await wert.json()
    werte.append(new_wert);
    
    return {
        "status" : "SUCCESS",
        "data" : new_wert
    }
    

@app.delete("/werte/{id}")
async def deleteWert(id: int):
    for w in werte:
        if w['id'] == id:
            werte.remove(w)
            return {
                "status" : "SUCCESS"
            }
    return {}