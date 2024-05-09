from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import model
from app.schemas import schema
from sqlalchemy.exc import SQLAlchemyError

def createLocation(location:schema.LocationCreate,db: Session):
    try:
        location_instance=model.Location(**location.model_dump())
        db.add(location_instance)
        db.commit()
        db.refresh(location_instance)
        return {
            'code': 200,
            'status': 'created successfully',
            'message': 'Data has been created successfully',
            'data':location_instance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))
    
def updateLocationById(locationId:int,location:schema.LocationCreate,db:Session):
    try:
        location_data=db.query(model.Location).filter(model.Location.id==locationId).first()
        if not location_data:
            raise HTTPException(status_code=404, detail="Location not found")
        location_data.location_name=location.location_name
        db.commit()
        return {
            'code': 200,
            'status': 'updated successfully',
            'message': 'Data has been updated successfully',
            'data':schema.GetLocationById.model_validate(location_data) 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def deleteLocationById(locationId:int,db:Session):
    try:
        location_data = db.query(model.Location).filter(model.Location.id == locationId).first()
        if not location_data:
            raise HTTPException(status_code=404, detail="Location not found")
        db.delete(location_data)
        db.commit()
        return {
            'code': 200,
            'status': 'deleted successfully',
            'message': 'Data has been deleted successfully',
            'data':{}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def getLocation(db:Session):
    try:
        return {
            'code':200,
            'status':'fetched successfully',
            'message':'all locations retrieved successfully',
            'data':db.query(model.Location).all()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def getLocationById(id:int,db:Session):
    try:
        return {
            'code':200,
            'status':'fetched successfully',
            'message':'location retrieved successfully',
            'data':db.query(model.Location).filter(id==id).first()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))


def create_ordersource(order_source:schema.OrderSourceCreate,db:Session):
    try:
        order_source_instance=model.OrderSource(**order_source.model_dump())
        db.add(order_source_instance)
        db.commit()
        db.refresh(order_source_instance)
        return {
            'code': 200,
            'status': 'created successfully',
            'message': 'Data has been created successfully',
            'data':order_source_instance.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def updateOrderSourceById(orderSourceId:int,orderSource:schema.OrderSourceCreate,db:Session):
    try:
        orderSourceData=db.query(model.OrderSource).filter(model.OrderSource.id==orderSourceId).first()
        if not orderSourceData:
            raise HTTPException(status_code=404, detail="orderSource not found")
        orderSourceData.order_source_name=orderSource.order_source_name
        db.commit()
        return {
            'code': 200,
            'status': 'updated successfully',
            'message': 'Data has been updated successfully',
            'data':schema.GetOrderSource.model_validate(orderSourceData)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def deleteOrderSourceById(orderSourceId:int,db:Session):
    try:
        orderSourceData = db.query(model.OrderSource).filter(model.OrderSource.id == orderSourceId).first()
        if not orderSourceData:
            raise HTTPException(status_code=404, detail="OrderSource not found")
        db.delete(orderSourceData)
        db.commit()
        return {
            'code': 200,
            'status': 'deleted successfully',
            'message': 'Data has been deleted successfully',
            'data':{}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def getOrderSources(db:Session):
    try:
        return {
            'code':200,
            'status':'fetched successfully',
            'message':'all locations retrieved successfully',
            'data':db.query(model.OrderSource).all()
            }
            # data_to_validate = {
            #         'code': 200,
            #         'status': 'fetched successfully',
            #         'message': 'all locations retrieved successfully',
            #         'data': order_sources
            #     }
                
            #     # Validate the JSON data against the Pydantic schema
            #     schema.GetOrderSource.model_validate_json(**data_to_validate)
                
            #     return data_to_validate
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def getOrderSource(id:int,db:Session):
    try:
        return {
            'code':200,
            'status':'fetched successfully',
            'message':'location retrieved successfully',
            'data':db.query(model.OrderSource).filter(id==id).first()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))

def create_vendor(vendor: schema.VendorCreate, db: Session):
    try:
        with db.begin():
            vendor_instance = model.Vendor(
                vendor_name=vendor.vendorName,
                active=vendor.active,
                createdBy=vendor.createdBy,
                lastUpdatedBy=vendor.lastUpdatedBy
            )
            db.add(vendor_instance)
            db.flush()

            if vendor.locations:
                for location in vendor.locations:
                    location_instance = model.VendorLocation(
                        locationId=location.locationId,
                        zip_code=location.zipCode,
                        isCurrent=location.isCurrent,
                        vendorId=vendor_instance.id
                    )
                    db.add(location_instance)
                    db.flush()

                    if location.orderSources:
                        for orderSource in location.orderSources:
                            order_source_instance = model.VendorOrderSource(
                                orderSourceId=orderSource.orderSourceId,
                                locationId=location_instance.id,
                                vendorId=vendor_instance.id
                            )
                            db.add(order_source_instance)
                            db.flush()
        db.commit()
        return {
            'code': 200,
            'status': 'created successfully',
            'message': 'Vendor created successfully',
            # 'data':schema.VendorGet.model_validate(vendor_instance)
            # db.query(model.Vendor).filter(model.Vendor.id==vendor_instance.id).first()
        }
    except SQLAlchemyError as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail="An error occurred while creating the vendor: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the vendor: " + str(e))