from fastapi import APIRouter, HTTPException, Depends, status,Path,Query
from typing import Annotated
from .. import  schema,utils,outh2
from ..repository.device import DeviceRepository
from ..schema import ResponseSchema,AddVlan,ChangeIntVlan,ChangeDesc
from ..repository.credential import CredentialRepository
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..NetOps import huawei,generic
import threading
import requests
router = APIRouter(prefix="/netops", tags=['NetOps'])

@router.get("/mac/{site_id}",response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def getMACAddress(
    current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],
    site_id: Annotated[int,Path(title="Site Id",ge=1)],
    ip: Annotated[str,Query(title="Switch IP or 'ALL' for a complete search")],
    mac: Annotated[str,Query(title="The mac Address to look for ",min_length=4, max_length=10)]
    ):
    credentials = await CredentialRepository.get_by_site_id(site_id=site_id)
    credentials = credentials._mapping
    if ip == "ALL":    
        devices = await DeviceRepository.get_switches_by_site_id(site_id=site_id)
        with ThreadPoolExecutor(max_workers=14) as excuter:
            future_list = []
            print(devices)
            for a_device in devices:
                connection = huawei.createConnection(a_device["ip"],credentials["username"],credentials["password"])
                if connection:
                    future = excuter.submit(huawei.getMacLocation, connection ,mac)
                    future_list.append(future)
            # Process as completed
            for future in as_completed(future_list) :
                print(future.result())
                if future.result():
                    result = future.result()
                    return ResponseSchema(detail=f"Successfully obtained a Port associated with this mac: {mac}",
                                    result=result)
        return ResponseSchema(detail=f"Failed to obtain a Port associated with this mac: {mac}")
    else:
        connection = huawei.createConnection(ip,credentials["username"],credentials["password"])
        if connection:
            result = huawei.getMacLocation(connection,mac)
            if result == None:
                return ResponseSchema(detail=f"Failed to obtain a Port associated with this mac: {mac}")
            return ResponseSchema(detail=f"Successfully obtained a Port associated with this mac: {mac}",
                                    result=result)
        else:
            return ResponseSchema(detail=f"Failed to obtain a connection with this switch :{ip} ")
        
        
@router.get('/siteavailability/{site_id}',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def get_Site_availability(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)], site_id: Annotated[int,Path(title="Site ID",ge=1)]):
    result = await generic.get_site_availability_threading(site_id)
    return ResponseSchema(detail="Successfully retrieved site's availability data !", result=result) 

@router.post("/addvlan/",response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_201_CREATED)
async def addVlan(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],operation: AddVlan):
    if current_user.user_type == 3:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    credentials = await CredentialRepository.get_by_site_id(operation.site_id)
    credentials = credentials._mapping
    connection = huawei.createConnection(operation.ip,credentials["username"],credentials["password"])
    if connection:
        return ResponseSchema(detail="Vlan added Successfully !", result=huawei.addVlan(connection,operation.vlanID,operation.vlan_desc,username=current_user.username))
    else:
        return ResponseSchema(detail=f"Failed to obtain a connection with this switch :{operation.ip} ")
    
@router.post("/changeintvlan/", response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_201_CREATED)
async def changeIntVlan(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],operation:ChangeIntVlan):
    credentials = await CredentialRepository.get_by_site_id(site_id=operation.site_id)
    credentials = credentials._mapping
    connection = huawei.createConnection(operation.ip, credentials["username"], credentials["password"])
    if connection:
        result = huawei.changeIntVlan(connection,operation.interfaceID, operation.vlanID,username=current_user.username)
        return ResponseSchema(detail=result["port_type"], result=result["output"])
    else:
        return ResponseSchema(detail="Couldn't connect to the switch please check log file")
    
@router.post("/intDesc/", response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_201_CREATED)
async def changeIntDesc(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],operation:ChangeDesc):
    if current_user.user_type == 3:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)    
    credentials = await CredentialRepository.get_by_site_id(site_id=operation.site_id)
    credentials = credentials._mapping
    connection = huawei.createConnection(operation.ip, credentials["username"], credentials["password"])
    if connection:
        result = huawei.changeIntDesc(connection,operation.interfaceID, operation.int_desc,username=current_user.username)
        return ResponseSchema(detail="The Interface Description Changed Successfully", result=result)
    else:
        return ResponseSchema(detail="Couldn't connect to the switch please check log file")
    


@router.get('/dashboard/{site_id}',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def get_Site_availability(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)], site_id: Annotated[int,Path(title="Site ID",ge=1)]):
    result = await generic.dashboardData(site_id)
    return ResponseSchema(detail="Successfully retrieved site's availability data !", result=result) 

@router.post('/pricechecker', response_model=ResponseSchema)
async def price_checker_update(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)]):
    try:
        result = requests.post("http://10.100.3.170:8840/api/v1/items")
        return ResponseSchema(detail="Successfully sent the sync request", result=result.json()["message"])
    except Exception:
        return ResponseSchema(detail="An Error occurred", result=Exception)

