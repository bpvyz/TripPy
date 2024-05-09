from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

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

    businesses = relationship("Business", cascade="all, delete-orphan", backref="owner")
    created_routes = relationship("Route", cascade="all, delete-orphan", backref="creator")

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

    location = relationship("Location")
    route_locations = relationship("RouteLocation", cascade="all, delete-orphan")

class BusinessRequest(db.Model):
    __tablename__ = 'businessesrequests'
    businessrequestid = db.Column(db.Integer, primary_key=True)
    businessname = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    locationid = db.Column(db.Integer, db.ForeignKey('locations.locationid'))
    ownerid = db.Column(db.Integer, db.ForeignKey('users.userid'))

    location = db.relationship("Location")

class Route(db.Model):
    __tablename__ = 'routes'
    routeid = db.Column(db.Integer, primary_key=True)
    routename = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    createdby = db.Column(db.Integer, db.ForeignKey('users.userid'))

    route_locations = relationship("RouteLocation", cascade="all, delete-orphan")
    route_participants = relationship("RouteParticipant", cascade="all, delete-orphan")

class RouteLocation(db.Model):
    __tablename__ = 'routelocations'
    routeid = db.Column(db.Integer, db.ForeignKey('routes.routeid'), primary_key=True)
    locationid = db.Column(db.Integer, db.ForeignKey('locations.locationid'), primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.businessid'))

    business = relationship("Business", overlaps="route_locations")

class RouteParticipant(db.Model):
    __tablename__ = 'routeparticipants'
    routeid = db.Column(db.Integer, db.ForeignKey('routes.routeid'), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), primary_key=True)
