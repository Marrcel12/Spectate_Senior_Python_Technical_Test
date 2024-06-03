from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Sport(Base):
    __tablename__ = 'sports'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    active = Column(Boolean, default=True)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    active = Column(Boolean, default=True)
    type = Column(String)
    sport_id = Column(Integer, ForeignKey('sports.id'))
    status = Column(String)
    scheduled_start = Column(DateTime)
    actual_start = Column(DateTime, nullable=True)
    sport = relationship("Sport", back_populates="events")

class Selection(Base):
    __tablename__ = 'selections'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    price = Column(Float)
    active = Column(Boolean, default=True)
    outcome = Column(String, default="Unsettled")
    event = relationship("Event", back_populates="selections")

Sport.events = relationship("Event", order_by=Event.id, back_populates="sport")
Event.selections = relationship("Selection", order_by=Selection.id, back_populates="event")
