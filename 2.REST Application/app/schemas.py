from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SportCreate(BaseModel):
    name: str

class SportUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None

class Sport(BaseModel):
    id: int
    name: str
    slug: str
    active: bool

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    name: str
    type: str
    sport_id: int
    scheduled_start: datetime

class EventUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None
    status: Optional[str] = None

class Event(BaseModel):
    id: int
    name: str
    slug: str
    active: bool
    type: str
    sport_id: int
    status: str
    scheduled_start: datetime
    actual_start: Optional[datetime]

    class Config:
        from_attributes = True

class SelectionCreate(BaseModel):
    name: str
    event_id: int
    price: float

class SelectionUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None
    outcome: Optional[str] = None

class Selection(BaseModel):
    id: int
    name: str
    event_id: int
    price: float
    active: bool
    outcome: str

    class Config:
        from_attributes = True
