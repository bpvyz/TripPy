from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    usertype = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phonenumber = db.Column(db.String(20))
    profilna = db.Column(db.String(255))

    businesses = relationship("Business", cascade="all, delete-orphan", backref="owner")
    businessrequests = relationship("BusinessRequest", cascade="all, delete-orphan", backref="owner")
    created_routes = relationship("Route", cascade="all, delete-orphan", backref="creator")
    route_participants = relationship("RouteParticipant", cascade="all, delete-orphan", backref="user")

class Location(db.Model):
    __tablename__ = 'locations'
    locationid = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)

class Business(db.Model):
    __tablename__ = 'businesses'
    businessid = db.Column(db.Integer, primary_key=True)
    businessname = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    locationid = db.Column(db.Integer, db.ForeignKey('locations.locationid'))
    ownerid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    image_path = db.Column(db.String(255))
    cena = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='RSD')

    location = relationship("Location")
    route_locations = relationship("RouteLocation", cascade="all, delete-orphan")

class BusinessRequest(db.Model):
    __tablename__ = 'businessesrequests'
    businessrequestid = db.Column(db.Integer, primary_key=True)
    businessname = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    locationid = db.Column(db.Integer, db.ForeignKey('locations.locationid'))
    ownerid = db.Column(db.Integer, db.ForeignKey('users.userid'))
    image_path = db.Column(db.String(255))
    cena = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='RSD')

    location = db.relationship("Location")

class Route(db.Model):
    __tablename__ = 'routes'
    routeid = db.Column(db.Integer, primary_key=True)
    routename = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    createdby = db.Column(db.Integer, db.ForeignKey('users.userid'))
    public = db.Column(db.String(255))

    __table_args__ = (
        CheckConstraint("public IN ('public', 'private')"),
    )

    route_locations = relationship("RouteLocation", cascade="all, delete-orphan")
    route_participants = relationship("RouteParticipant", cascade="all, delete-orphan")

class RouteLocation(db.Model):
    __tablename__ = 'routelocations'
    routeid = db.Column(db.Integer, db.ForeignKey('routes.routeid'), primary_key=True)
    locationid = db.Column(db.Integer, db.ForeignKey('locations.locationid'), primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.businessid'), primary_key=True)
    day = db.Column(db.Integer)

    location = relationship("Location")
    business = relationship("Business", overlaps="route_locations")

class RouteParticipant(db.Model):
    __tablename__ = 'routeparticipants'
    routeid = db.Column(db.Integer, db.ForeignKey('routes.routeid'), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), primary_key=True)
