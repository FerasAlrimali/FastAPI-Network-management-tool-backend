from datetime import date
from pydantic import BaseModel,Field
from typing import TypeVar, Generic, List,Optional,Union
from pydantic.generics import GenericModel
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
T = TypeVar('T')

class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None

class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """
    page_number: int  = Field(gt=0)
    page_size: int = Field(gt=0)
    total_pages: int = Field(gt=0)
    total_records: int = Field(gt=0)
    content: List[dict]

class UserCreate(BaseModel):
    username: str
    hashed_password: str
    authorization: int = Field(gt=0, lt=4)
    site_id: int = Field(gt=0)

class SiteCreate(BaseModel):
    site_name: str

class CredentialCreate(BaseModel):
    username: str
    password: str
    site_id: int = Field(gt=0)

class DeviceTypeCreate(BaseModel):
    device_type: str

class DeviceModelCreate(BaseModel):
    device_model: str
    deviceType_id: int = Field(gt=0)

class DeviceCreate(BaseModel):
    ip: str 
    name: str
    site_id: int = Field(gt=0)
    deviceModel_id: int = Field(gt=0)

class VlanCreate(BaseModel):
    vlan_id: int = Field(gt=0)
    vlan_desc: str
    site_id: int = Field(gt=0)

class Operation(BaseModel):
    ip : str
    site_id : int = Field(gt=0)

class AddVlan(Operation):
    vlanID: int = Field(gt=0)
    vlan_desc: str
    
class ChangeIntVlan(Operation):
    interfaceID: int = Field(gt=0, lt=49)
    vlanID: int = Field(gt=0, lt=4000)

class ChangeDesc(Operation):
    interfaceID: int = Field(gt=0, lt=49)
    int_desc :  str  

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    site_id:  Union[int, None] = None
    user_type:Union[int, None] = None

class LoginUser(BaseModel):
    username: str
    password: str

class TestHome(BaseModel):
    result: str

class DeviceOut(BaseModel):
    ip: str
    name: str
    device_type: str
    device_model: str
    id: int


# class DeviceFilter(Filter):
#     name: Optional[str] = None
#     name__ilike: Optional[str] = None
#     name__like: Optional[str] = None
#     name__neq: Optional[str] = None
#     device_type: Optional[str] = None
#     device_type__ilike: Optional[str] = None
#     device_type__like: Optional[str] = None
#     device_type__neq: Optional[str] = None
#     age__lt: Optional[int] = None
#     age__gte: int = Field(Query(description="this is a nice description"))
#     """Required field with a custom description.

#     See: https://github.com/tiangolo/fastapi/issues/4700 for why we need to wrap `Query` in `Field`.
#     """
#     order_by: list[str] = ["age"]
#     search: Optional[str] = None

#     class Constants(Filter.Constants):
#         model = User
#         search_model_fields = ["name"]