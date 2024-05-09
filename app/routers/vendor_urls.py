from app.dependency import get_db
from sqlalchemy.orm import Session
from app.apis.vendors import vendorApi
from fastapi import APIRouter,Depends
from app.schemas.schema import VendorCreate,LocationCreate,OrderSourceCreate,GetLocations
router = APIRouter()
@router.post("/vendor/")
def create_item(vendor: VendorCreate, db: Session = Depends(get_db)):
    data = vendorApi.create_vendor(vendor,db)
    return data

@router.post("/location/")
def createLocation(location: LocationCreate, db: Session = Depends(get_db)):
    data = vendorApi.createLocation(location,db)
    return data

@router.get("/location/")
def getAllLocations(db: Session = Depends(get_db)):
    data = vendorApi.getLocation(db)
    return data

@router.get("/location/{id}")
def getLocationById(id:int,db: Session = Depends(get_db)):
    data = vendorApi.getLocationById(id,db)
    return data

@router.put("/location/{id}")
def updateLocationById(id:int,location:LocationCreate,db: Session = Depends(get_db)):
    data = vendorApi.updateLocationById(id,location,db)
    return data

@router.delete("/location/{id}")
def updateLocationById(id:int,db: Session = Depends(get_db)):
    data = vendorApi.deleteLocationById(id,db)
    return data

@router.post("/order-source/")
def create_item(order_source: OrderSourceCreate, db: Session = Depends(get_db)):
    data = vendorApi.create_ordersource(order_source,db)
    return data

@router.put("/order-source/{id}")
def updateLocationById(id:int,orderSource:OrderSourceCreate,db: Session = Depends(get_db)):
    data = vendorApi.updateOrderSourceById(id,orderSource,db)
    return data

@router.get("/order-source/")
def getAllLocations(db: Session = Depends(get_db)):
    data = vendorApi.getOrderSources(db)
    return data

@router.get("/order-source/{id}")
def getOrderSourceById(id:int,db: Session = Depends(get_db)):
    data = vendorApi.getOrderSource(id,db)
    return data
@router.delete("/order-source/{id}")
def updateOrderSourceById(id:int,db: Session = Depends(get_db)):
    data = vendorApi.deleteOrderSourceById(id,db)
    return data