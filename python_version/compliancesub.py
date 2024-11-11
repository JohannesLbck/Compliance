#! /usr/bin/python
import uvicorn
import os
import signal
import sys
from fastapi import FastAPI, File, UploadFile, Request
from multiprocessing import Process
from fastapi.responses import HTMLResponse, JSONResponse


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
async def Subscriber(data: Request):
    json = await data.body()
    print(json)
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

