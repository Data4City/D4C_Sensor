from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Kit(Base):
    __tablename__ = "kit"
    #TODO Add geolocation
    id = Column('id', Integer, primary_key=True)
    serial = Column('serial', String(16))
    sensors_used = relationship('Sensor')
    measurement_data = relationship('Value')

class Sensor(Base):
    __tablename__ = "sensor"
    id = Column('id', Integer, primary_key=True)
    name = Column("name",String(40))
    model = Column("model", String(40))
    kit_id = Column(Integer, ForeignKey('kit.id'))
    measurements = relationship('Measurement')

class Measurement(Base):    
    __tablename__ = "measurement"
    id = Column('id', Integer, primary_key=True)
    used_by = Column(Integer, ForeignKey('sensor.id'), nullable= False)
    symbol = Column('symbol', String(5))
    name = Column('name', String(30))

class Value(Base):
    __tablename__ = "value"
    id = Column('id', Integer, primary_key=True)
    data  = Column("data", Float)
    timestamp = Column("timestamp", DateTime(timezone=True))
    belongs_to = Column(Integer, ForeignKey('kitm.id'), nullable= False)
    measurement = Column(Integer, ForeignKey('measurement.id'), nullable= False)
    
if __name__ == "__main__":
    engine = create_engine("sqlite:///sensor.db", echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)