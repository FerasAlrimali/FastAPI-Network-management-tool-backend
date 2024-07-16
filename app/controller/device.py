from fastapi import APIRouter,Query, Path, Depends, HTTPException,status
from app.schema import  ResponseSchema,DeviceCreate
from .. import  schema,utils,outh2
from app.repository.device import DeviceRepository
from typing import Annotated
router = APIRouter(prefix="/device", tags=["Devices"])

@router.post('/',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_201_CREATED)
async def creat(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],create_form: DeviceCreate):
    if current_user.user_type == 3:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceRepository.create(create_form=create_form)
    return ResponseSchema(detail="Successfully created data !")

@router.patch('/{id}',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def update(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],id: Annotated[int, Path(title="device ID",ge=1)], update_form: DeviceCreate):
    if current_user.user_type == 3:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceRepository.update(device_id=id,update_form=update_form)
    return ResponseSchema(detail="Successfully updated data !")

@router.delete('/{id}',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def delete(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],id: Annotated[int, Path(title="device ID",ge=1)]):
    if current_user.user_type == 3:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceRepository.delete(device_id=id)
    return ResponseSchema(detail="Successfully deleted data !")

@router.get('/{site_id}',response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def get_by_site_id(
    current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],
    site_id: Annotated[int,Path(title="Site ID",ge=1)],
    page: Annotated[int, Query(title="Page no", ge=1)] = 1,
    limit: Annotated[int, Query(title="The limit of lines per page",ge=1)]  = 10,
    columns: Annotated[str | None, Query(alias="columns")] = None ,
    sort: Annotated[str | None, Query(alias="sort")] = None,
    filter: Annotated[str | None, Query(alias="filter")] = None
    ):
    result = await DeviceRepository.get_all_by_site_id(site_id=site_id,
                        page=page,limit=limit,columns=columns,sort=sort,filter=filter)
    
    return ResponseSchema(detail="Successfully fetch data !",result=result)

@router.get('/{site_id}/{device_type}',response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def get_by_site_id(
    current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],
    site_id: int = Path(title="The id of the Site",ge=1),
    device_type: str = Path(title="Device Type Switch or Router as an ex"),
    page: Annotated[int, Query(title="Page Number",ge=1)] = 1,
    limit: Annotated[int, Query(title="Lines per page",ge=1)]  = 10,
    columns: Annotated[str | None, Query(alias="columns")] = None ,
    sort: Annotated[str | None, Query(alias="sort")] = None,
    filter: Annotated[str | None, Query( alias="filter")] = None
    ):
    result = await DeviceRepository.get_by_device_type_and_site_id(site_id=site_id,device_type=device_type,
                        page=page,limit=limit,columns=columns,sort=sort,filter=filter)
    
    return ResponseSchema(detail="Successfully fetch data !",result=result)
    
    
