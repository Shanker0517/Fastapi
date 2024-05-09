from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional

class Status(BaseModel):
    Active: str = 'active'
    Inactive: str = 'inactive'

class TimeStamp(BaseModel):
    createdDate: datetime
    lastUpdatedDate: datetime

class OrderSourceCreate(BaseModel):
    orderSourceName: str

class GetOrderSource(BaseModel):
    id:int
    orderSourceName: str
    class Config:
        from_attributes=True

# class GetOrderSource(BaseModel):
#     code:int
#     status:str
#     message:str
#     data:List[GetOrderSource]|GetOrderSource



class LocationCreate(BaseModel):
    locationName: str

class GetLocationById(BaseModel):
    id:int
    locationName:str
    class Config:
        orm_mode = True
        from_attributes=True




class VendorOrderSourceCreate(BaseModel):
    orderSourceId: int
    class Config:
        orm_mode = True

class VendorLocationCreate(BaseModel):
    locationId: int
    zipCode: str
    isCurrent: str='0'
    orderSources: Optional[List[VendorOrderSourceCreate]] = None
    class Config:
        orm_mode = True

class VendorCreate(BaseModel):  
    vendorName: str
    active: str
    createdBy: int
    lastUpdatedBy: int
    locations: Optional[List[VendorLocationCreate]] = None 
    class Config:
        orm_mode = True


class GetOrderSources(BaseModel):
    id:int
    orderSourceName: str
    vendorId:int
    locationId:int

class GetLocations(BaseModel):
    id:int
    locationName:str
    isCurrent:str
    orderSources:Optional[List[GetOrderSources]] = None 
    vendorId:int

class VendorGet(TimeStamp):
    id:int
    vendorName: str
    active: str
    createdBy: int
    lastUpdatedBy: int
    locations: Optional[List[GetLocations]] = None 

class SuccessResponse(BaseModel):
    code:int
    status:str
    message:str
    data:List[VendorGet] | VendorGet

class FailureResponse(BaseModel):
    code:int
    status:str
    message:str
    error:str