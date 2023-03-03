#main
#  start local e.g.: python3 -m uvicorn main:app --reload --port 8000
#  ein schöner Kommentar
from fastapi import FastAPI, Request
from datetime import datetime, timedelta

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
    
    #handle id
    try:
        current_id=new_wert['id']
    except:
        #find next id
        max=werte[0]['id']
        for w in werte:
            if (int(w['id'])>max):
                max = w['id']
        new_wert['id']=max+1
    
    #handle tstamp
    try:
        current_tstamp=new_wert['tstamp']
    except:
        #no tstamp
        # "2023-03-03 09:53:00"
        current_tstamp = (datetime.now()+ timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        new_wert['tstamp']=current_tstamp
    
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