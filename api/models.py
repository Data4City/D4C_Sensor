from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Box(Base):
    __tablename__ = "box"
    serial = Column('serial', String(16), primary_key=True)

class Sensors(Base):
    __tablename__ = "sensor"
    id = Column('id', Integer, primary_key=True)
    name = Column("name",String(40))
    model = Column("model", String(40))

class Unit(Base):
    __tablename__ = "unit"
    symbol = Column('symbol', String(5), primary_key=True)
    name = Column('name', String(30))

class Measurement(Base):
    __tablename__ = "measurement"
    id = Column('id', Integer, primary_key=True)
    value = Column("value", Float)
    timestamp = Column("timestamp", DateTime(timezone=True))
    sensor_id = Column(Integer, ForeignKey('sensor.id'), nullable= False)
    unit_id = Column(Integer, ForeignKey('unit.symbol'), nullable= False)
    box_serial = Column(Integer, ForeignKey('box.serial'), nullable= False)

if __name__ == "__main__":
    engine = create_engine("sqlite:///sensor.db", echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)