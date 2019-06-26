import datetime

from app import db
from app.base_model import BaseModel


class Airport(BaseModel):
    """This class defines the airports table"""

    __tablename__ = 'airports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(256), nullable=False)
    flights = db.relationship('Flight', backref='airport',
                              order_by='flight_schedules.id',
                              cascade="all, delete-orphan", lazy=True)

    def __init__(self, name, country, city):
        """Initialize the airport with the airport details"""
        self.name = name
        self.country = country
        self.city = city

    def __repr__(self):
        return 'airpots: {}'.format(self.name)


class Airplane(BaseModel):
    """This class defines the airplanes table"""

    __tablename__ = 'airplanes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_number = db.Column(db.Integer, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    economy_seats = db.Column(db.Integer, nullable=False)
    business_seats = db.Column(db.Integer, nullable=False)
    first_class_seats = db.Column(db.Integer, nullable=False)
    flights = db.relationship('Flight', backref='airplane',
                              order_by='flight_schedules.id',
                              cascade="all, delete-orphan", lazy=True)

    def __init__(self, reg_number, economy_seats, business_seats=0,
                 first_class_seats=0):
        """Initialize the airplane details"""
        self.reg_number = reg_number
        self.total_seats = economy_seats + business_seats + first_class_seats
        self.economy_seats = economy_seats
        self.business_seats = business_seats
        self.first_class_seats = first_class_seats

    def __repr__(self):
        return 'Airplane: {}'.format(self.reg_number)


class Flight(BaseModel):
    """This class defines the flight schedules table"""

    __tablename__ = 'flight_schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departure_date = db.Column(db.DateTime, nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'),
                                     nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'),
                                   nullable=False)
    status = db.Column(db.String(256), default='upcoming')
    airplane = db.Column(db.Integer, db.ForeignKey('airplanes.id'),
                         nullable=False)
    booked_first = db.Column(db.Integer, default=0)
    booked_business = db.Column(db.Integer, default=0)
    booked_economy = db.Column(db.Integer, default=0)
    bookings = db.relationship('Booking', backref='flight',
                               order_by='bookings.id',
                               cascade="all, delete-orphan", lazy=True)

    def __init__(self, departure_date, departure_airport_id, arrival_date,
                 arrival_airport_id, airplane):
        """Initialize the flight details"""
        self.departure_date = departure_date
        self.departure_airport_id = departure_airport_id
        self.arrival_date = arrival_date
        self.arrival_airport_id = arrival_airport_id
        self.airplane = airplane

    def __repr__(self):
        return 'Flight: {}'.format(self.id)
