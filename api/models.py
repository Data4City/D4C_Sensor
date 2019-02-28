from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload
from datetime import datetime

Base = declarative_base()

sensors_in_kit = Table('sensors_in_kit', Base.metadata,
    Column('kit_id', Integer, ForeignKey('kit.id')),
    Column('sensor_id', Integer, ForeignKey('sensor.id'))
)


class Kit(Base):
    __tablename__ = "kit"
    # TODO Add geolocation
    id = Column('id', Integer, primary_key=True)
    serial = Column('serial', String(16))
    created_at = Column("timestamp", DateTime(timezone=True), default=datetime.now())
    sensors_used = relationship('Sensor', secondary=sensors_in_kit, backref='kits', lazy='dynamic')

    # measurement_data = relationship('Value', backref="kit")

    def __init__(self, serial):
        self.serial = serial

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'sensors_used': [s.as_dict for s in self.sensors_used]
        }

    @classmethod
    def get_values_from_kit(self, session, amount: int = 0):
        return_value = {}
        for sensor in self.sensors_used:
            for measurement in sensor.measurements:
                if amount <= 0:
                    return_value[sensor.name] = session.query(Value).filter(Value.measurement == measurement.id).all()
                else:
                    return_value[sensor.name] = session.query(Value).filter(Value.measurement == measurement.id).limit(
                        amount)
        return return_value

    def save(self, session):
        session.add(self)
        session.commit()


class Sensor(Base):
    __tablename__ = "sensor"
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(40), nullable=False)
    model = Column("model", String(40), nullable=False)
    #kit_id = Column(Integer, ForeignKey('kit.id'))
    measurements = relationship('Measurement')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model
        }

    def add_kit(self, kit):
        self.kits.append(kit)
        self.session.commit()

    def save(self, session):
        session.add(self)
        session.commit()


class Measurement(Base):
    __tablename__ = "measurement"
    id = Column('id', Integer, primary_key=True)
    measured_by = Column(Integer, ForeignKey('sensor.id'), nullable=False)
    symbol = Column('symbol', String(5))
    name = Column('name', String(30))

    @property
    def as_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name,
        }

    def save(self, session):
        session.add(self)
        session.commit()


class Value(Base):
    __tablename__ = "value"
    id = Column('id', Integer, primary_key=True)
    data = Column("data", Float)
    timestamp = Column("timestamp", DateTime(timezone=True))
    belongs_to = Column(Integer, ForeignKey('kit.id'), nullable=False)
    measurement = Column(Integer, ForeignKey('measurement.id'), nullable=False)

    @property
    def as_dict(self):
        return {
            'timestamp': self.timestamp,
            'data': self.data,
            'symbol': self.measurement.symbol
        }

    def save(self, session):
        session.add(self)
        session.commit()


def __reset_db__():
    engine = create_engine("sqlite:///sensor.db", echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    __reset_db__()
