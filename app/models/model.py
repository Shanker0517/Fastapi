import enum
from app.db import Base
from sqlalchemy import Enum
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import declared_attr,mapped_column, relationship
"""
Vendor Model
 vendorId: number;
  vendorName: string;
  active: number;
  createdBy: string;
  createdDate: string;
  lastUpdatedBy: string;
  lastUpdatedDate: string;
  locations: LocationRecord[];


Location Model
  locationId: number;
  locationName: string;
  locationZipCode: number;
  isCurrent: number;
  orderSources: OrderSourceRecord[];

OrderSource Model
  orderSourceId: number;
  orderSourceName: string;

  parameter of Column server_default use of this is getting the default value but from server side like timestamp for server
"""
class Status(enum.Enum):
    # left one is for Database
    Active = 'active'
    Inactive = 'inactive'

class TimeStamp:
    @declared_attr
    def createdDate(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def lastUpdatedDate(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now())

    class Meta:
        abstract = True


# class Vendor(Base):
#     __tablename__ = 'vendor'

#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
#     vendor_name = Column(String(50), nullable=False)
#     active = Column(Enum(Status), nullable=False, default=Status.Active.value)
#     _locations = relationship('Location', back_populates='_vendor')  # Updated attribute name
#     createdBy = Column(Integer, nullable=False)
#     lastUpdatedBy = Column(Integer, nullable=False)

# class Location(Base):
#     __tablename__ = 'location'
#     id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
#     location_name = Column(String(150), nullable=False)
#     zip_code = Column(String(150), nullable=False)
#     is_current = Column(Enum('0', '1'), default='0')
#     vendor_id = Column(Integer, ForeignKey('vendor.id'), nullable=False)
#     _vendor = relationship('Vendor', back_populates='_locations')  # Use back_populates
#     _order_sources = relationship('OrderSource', back_populates='_location', uselist=True)

# class OrderSource(Base):
#     __tablename__='order_source'
#     id=Column(Integer, nullable=False, primary_key=True, autoincrement=True)
#     ordersource_name=Column(String(150), nullable=False)
#     location_id=Column(Integer, ForeignKey('location.id'), nullable=False)
#     _location=relationship('Location', back_populates='_order_sources')  # Use back_populates

# class Location(Base):
#     __tablename__ = 'location'

#     id=Column(Integer,nullable=False, primary_key=True, autoincrement=True)
#     location_name = Column(String(150), nullable=False)

# class OrderSource(Base):
#     __tablename__ = 'order_source'
    
#     id=Column(Integer,nullable=False, primary_key=True, autoincrement=True)
#     order_source_name=Column(String(255),nullable=False)

# class Vendor(Base):
#     __tablename__ = 'vendor'

#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
#     vendor_name = Column(String(50), nullable=False)
#     active = Column(Enum(Status), nullable=False, default=Status.Active.value)
#     createdBy = Column(Integer, nullable=False)
#     lastUpdatedBy = Column(Integer, nullable=False)
#     locations = relationship('VendorLocation', back_populates='vendor', uselist=True)


# class VendorLocation(Base):
#     __tablename__ = 'vendor_locations'

#     id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
#     location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
#     zip_code = Column(String(150), nullable=False)
#     is_current = Column(Enum('0', '1'), default='0')
#     vendor_id = Column(Integer, ForeignKey('vendor.id'), nullable=False)
#     vendor = relationship('Vendor', back_populates='locations')  
#     order_sources = relationship('VendorOrderSource', back_populates='locations', uselist=True)

# class VendorOrderSource(Base):
#     __tablename__='vendor_ordersources'
    
#     id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
#     order_source_id = Column(Integer, ForeignKey('order_source.id'), nullable=False)
#     location_id=Column(Integer, ForeignKey('location.id'),nullable=False)
#     locations=relationship('VendorLocation',back_populates='order_sources')
#     vendor_id = Column(Integer, ForeignKey('vendor.id'), nullable=False)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(150), nullable=False)

    def to_dict(self):
        """
        Convert SQLAlchemy model instance to a dictionary
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class OrderSource(Base):
    __tablename__ = 'order_source'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_source_name = Column(String(255), nullable=False)

    def to_dict(self):
        """
        Convert SQLAlchemy model instance to a dictionary
        Model Methods:
        Custom Methods: SQLAlchemy models can define custom methods for encapsulating business logic, similar to Django models.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Vendor(Base):
    __tablename__ = 'vendor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_name = Column(String(50), nullable=False)
    active = Column(Enum(Status), nullable=False, default=Status.Active.value)
    createdBy = Column(Integer, nullable=False)
    lastUpdatedBy = Column(Integer, nullable=False)
    locations = relationship('VendorLocation', back_populates='vendor', cascade='all, delete-orphan')

class VendorLocation(Base):
    __tablename__ = 'vendor_location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    locationId = Column(Integer, ForeignKey('location.id'), nullable=False)
    zip_code = Column(String(150), nullable=False)
    isCurrent = Column(Enum('0', '1'), default='0')
    vendorId = Column(Integer, ForeignKey('vendor.id'), nullable=False)
    vendor = relationship('Vendor', back_populates='locations')  
    order_sources = relationship('VendorOrderSource', back_populates='location', cascade='all, delete-orphan')

class VendorOrderSource(Base):
    __tablename__ = 'vendor_order_source'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    orderSourceId = Column(Integer, ForeignKey('order_source.id'), nullable=False)
    locationId = Column(Integer, ForeignKey('vendor_location.id'), nullable=False)  # Foreign key referencing VendorLocation
    location = relationship('VendorLocation', back_populates='order_sources')
    vendorId = Column(Integer, ForeignKey('vendor.id'), nullable=False)

# class Parent1(Base):
#     __tablename__ = "parent_table"
#     id = mapped_column(Integer, primary_key=True)
#     children = relationship("Child", back_populates="parent")

# class Child1(Base):
#     __tablename__ = "child_table"
#     id = mapped_column(Integer, primary_key=True)
#     parent_id = mapped_column(ForeignKey("parent_table.id"))
#     parent = relationship("Parent", back_populates="children")

# class Parent2(Base):
#     __tablename__ = "parent_table2"
#     id = mapped_column(Integer, primary_key=True)
#     children = relationship("Child", back_populates="parent")

# class Child2(Base):
#     __tablename__ = "child_table2"
#     id = mapped_column(Integer, primary_key=True)
#     parent_id = mapped_column(ForeignKey("parent_table.id"))

# class TimestampMixin:
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
# class User(Base, TimestampMixin):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
