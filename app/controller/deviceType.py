from fastapi import APIRouter,Query,Path,Depends, HTTPException,status
from typing import Annotated
from .. import  schema,utils,outh2
from app.schema import  ResponseSchema,DeviceTypeCreate
from app.repository.devicetype import DeviceTypeRepository
router = APIRouter(prefix="/deviceType", tags=["DeviceType"])

@router.post('/',response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_201_CREATED)
async def create(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],create_form : DeviceTypeCreate):
    if current_user.user_type != 1:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceTypeRepository.create(create_form=create_form)
    return ResponseSchema(detail="Successfully created data !")

@router.patch('/{id}', response_model=ResponseSchema, response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def update(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],id: Annotated[int, Path(title="Device Type Id",ge=1)], update_form: DeviceTypeCreate):
    if current_user.user_type != 1:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceTypeRepository.update(deviceType_id=id, update_form=update_form)
    return ResponseSchema(detail="Successfully updated data !")

@router.delete('/{id}', response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def delete(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],id: Annotated[int, Path(title="Device Type Id",ge=1)],):
    if current_user.user_type != 1:
        raise HTTPException(detail="U are not allowed to access this route",status_code=status.HTTP_401_UNAUTHORIZED)
    await DeviceTypeRepository.delete(deviceType_id=id)
    return ResponseSchema(detail="Successfully deleted data !")

@router.get('/',response_model=ResponseSchema,response_model_exclude_none=True,status_code=status.HTTP_200_OK)
async def get_all(
    current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],
    page: Annotated[int, Query(title="Page no", ge=1)] = 1,
    limit: Annotated[int, Query(title="The limit of lines per page",ge=1)]  = 10,
    columns: Annotated[str | None, Query(alias="columns")] = None ,
    sort: Annotated[str | None, Query(alias="sort")] = None,
    filter: Annotated[str | None, Query(alias="filter")] = None
):
    result = await DeviceTypeRepository.get_all(page=page,limit=limit,columns=columns,sort=sort,filter=filter)
    return ResponseSchema(detail="successfully fetch all data !",result=result)
