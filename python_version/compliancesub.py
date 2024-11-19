#! /usr/bin/python
import uvicorn
import os
import signal
import sys
import json
import re
import xml.etree.ElementTree as ET
from fastapi import FastAPI, File, UploadFile, Request, Form
from pydantic import BaseModel
from multiprocessing import Process
from fastapi.responses import HTMLResponse, JSONResponse
from hashmap import HashTable
from tree_util import find_by_attribute

hash_t = HashTable(20)
hash_t.load_disk("TrackedUIDsHashmap.json")

class Model(BaseModel):
    cpee: str
    instance_url: str
    instance: int
    topic: str
    type: str
    name: str
    timestamp: str
    content: dict
    instance_uuid: str
    instance_name: str

app = FastAPI()

@app.get("/")
async def main():
    content = """
    <body>
    <form action="/Subscriber" enctype="multipart/form_data" method="post">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

@app.post("/Subscriber")
async def Subscriber(request: Request):
    async with request.form() as form:
        #print(form)
        notification = json.loads(form["notification"])
        hash_t.insert(notification["instance-uuid"], notification)
        try:
            requirements = notification["content"]["attributes"]["requirements"]
            print("reached")
        except:
            print("No requirements attribute was passed, nothing to check")
            return
        try:
            save = notification["content"]["attributes"]["save"]
            if save:
                hash_t.save_disk("TrackedUIDsHashmap.json")
        except:
            print("No save attribute was passed, previous version will only be stored in memory and not written to disk")
            print("If a save attribute was passed, and this message still shows, there is a internal server error")
        print(ET.tostring(ET.fromstring(notification["content"]["description"]), encoding='utf8').decode('utf8'))
        xml = ET.fromstring(notification["content"]["description"])
        typ3 = form["type"]
        topic = form["topic"]
        event = form["event"]
        #print(notification["content"]["dsl"])

    return

def run_server():
    pid = os.fork()
    if pid != 0:
        return
    print('Starting ' + str(os.getpid()))
    print(os.getpid(), file=open('compliancesub.pid', 'w'))
    uvicorn.run("compliancesub:app", port=9321, log_level="info")

if __name__ == "__main__":
    if os.path.exists('compliancesub.pid'):
      with open("compliancesub.pid","r") as f: pid =f.read()
      print('Killing ' + str(int(pid)))
      os.remove('compliancesub.pid')
      os.kill(int(pid),signal.SIGINT)
    else:
      proc = Process(target=run_server, args=(), daemon=True)
      proc.start()
      proc.join()

