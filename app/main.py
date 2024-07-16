from fastapi import FastAPI, Query
import uvicorn
from app.conf import db
from contextlib import asynccontextmanager
from .controller import user,site,credential,deviceType,deviceModel,device,vlan,netops,auth
from pydantic import Field
from typing import Annotated
from .schema import TestHome
from fastapi.middleware.cors import CORSMiddleware
from .repository.device import DeviceRepository
def init_app():
    db.init()

    @asynccontextmanager
    async def lifespan(app:FastAPI):
        await db.create_all()
        yield
        await db.close()
    
    app = FastAPI(title="NMv2", description="A network tool to manage network devices", version="2", lifespan=lifespan)
    origins = [
    "http://localhost:9999", "localhost", "*"
                        ]
    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    app.include_router(site.router)
    app.include_router(user.router)
    app.include_router(credential.router)
    app.include_router(deviceType.router)
    app.include_router(deviceModel.router)
    app.include_router(device.router)
    app.include_router(vlan.router)
    app.include_router(netops.router)
    app.include_router(auth.router)
    return app

app = init_app()
ip_regex = "^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"
from fastapi_filters.ext.sqlalchemy import apply_filters
from fastapi_filters import create_filters, create_filters_from_model, FilterValues
from fastapi import Depends
from .schema import DeviceOut
@app.get("/")
async def home(   filters: FilterValues = Depends(create_filters_from_model(DeviceOut)),
):
    result = await DeviceRepository.test(filters=filters)
    return result

def start():
    """A function to lunch the app through 'poetry run start' at root level"""
    uvicorn.run("app.main:app",host="localhost",port=9999, reload=True)