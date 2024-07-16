from fastapi import APIRouter,Query,Path,Depends, HTTPException,status
from .. import  schema,utils,outh2
from typing import Annotated
from app.schema import  ResponseSchema,DeviceModelCreate
from app.repository.deviceModel import DeviceModelRepository
router = APIRouter(prefix="/deviceModel", tags=["DeviceModel"])

@router.post('/',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_201_CREATED)
async def create(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],create_form: DeviceModelCreate):
    if current_user.user_type != 1:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceModelRepository.create(create_form=create_form)
    return ResponseSchema(detail="Successfully created data !")

@router.patch('/{id}',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def update(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],id: Annotated[int,Path(title="Device Moedel Id",ge=1)], update_form: DeviceModelCreate):
    if current_user.user_type != 1:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceModelRepository.update(deviceModel_id=id, update_form=update_form)
    return ResponseSchema(detail="Successfully updated data !")

@router.delete('/{id}',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def delete(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],id: Annotated[int,Path(title="The device model id",ge=1)]):
    if current_user.user_type != 1:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceModelRepository.delete(deviceModel_id=id)
    return ResponseSchema(detail="Successfully deleted data !")

@router.get('/{deviceType}',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def get_by_devicecType(
    current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],
    deviceType: Annotated[str,Path(title="Device Type Switch or Router as an ex")],
    page: Annotated[int, Query(title="Page no", ge=1)] = 1,
    limit: Annotated[int, Query(title="The limit of lines per page",ge=1)]  = 10,
    columns: Annotated[str | None, Query(alias="columns")] = None ,
    sort: Annotated[str | None, Query(alias="sort")] = None,
    filter: Annotated[str | None, Query(alias="filter")] = None
    ):
    result = await DeviceModelRepository.get_by_device_type(
        device_type=deviceType,
        page=page,limit=limit,columns=columns,sort=sort,filter=filter)
    
    return ResponseSchema(detail="Successfully fetch data !",result=result)

@router.get('/',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)   
async def get_all(
    current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],
    page: Annotated[int, Query(title="Page no", ge=1)] = 1,
    limit: Annotated[int, Query(title="The limit of lines per page",ge=1)]  = 10,
    columns: Annotated[str | None, Query(alias="columns")] = None ,
    sort: Annotated[str | None, Query(alias="sort")] = None,
    filter: Annotated[str | None, Query(alias="filter")] = None
            ):
    result = await DeviceModelRepository.get_all(
                        page=page,limit=limit,columns=columns,sort=sort,filter=filter)
    
    return ResponseSchema(detail="Successfully fetch data !",result=result)
