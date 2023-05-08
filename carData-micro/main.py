#main
#  start local e.g.: python3 -m uvicorn main:app --reload --port 8000
from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from fastapi_mqtt import FastMQTT, MQTTConfig
import json

#add track-id
werte = [{"tstamp": "2023-02-17 14:48:00","value": 42,"id": 1, "track": "1"},
           {"tstamp": "2023-02-17 14:49:00","value": 34,"id": 2, "track": "1"},
           {"tstamp": "2023-02-17 14:50:00","value": 17,"id": 3, "track": "1"}]

max_gps_werte = 100
gps_werte = []

app = FastAPI()

mqtt_config = MQTTConfig()
mqtt_config.host="broker.hivemq.com"
mqtt_config.port=1883
fast_mqtt = FastMQTT(mqtt_config)

fast_mqtt.init_app(app)


@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.subscribe("ima_test")
async def message_to_topic(client, topic, payload, qos, properties):
    #print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    gps_wertStr = payload.decode()
    gps_wert = json.loads(gps_wertStr)
    print(gps_wert)
    gps_werte.append(gps_wert);
    if (len(gps_werte)>max_gps_werte):
        gps_werte.pop(0)
    
    

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

#-------------------------------------------------------------------------------------------
@app.on_event("startup")
async def app_startup():
    print ("Server startd")
    

@app.get("/werte")
async def root_werte():
    print("in /werte")
    return werte

@app.get("/gpswerte")
async def root_werteGPS():
    return gps_werte

@app.get("/werte/latest")
async def read_werte_latest():
    #fget the last values
    l = len(werte)
    if l>0:
        return werte[l-1]
    else:
        return {}
    
@app.get("/gpswerte/latest")
async def read_gpswerte_latest():
    #fget the last values
    l = len(gps_werte)
    if l>0:
        return gps_werte[l-1]
    else:
        return {}
    
@app.get("/werte/track/{track_str}")
async def read_werte_forTrack(track_str: str):
    print("in function")
    retWerte=[]
    for w in werte:
        if w['track'] == track_str:
            retWerte.append(w);
    return retWerte

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