from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    total_rooms = Column(Integer, nullable = False)
    star_rating = Column(Float)
    created_at = Column(DateTime, default =datetime.utcnow)

    #relationships

    bookings = relationship("Booking", back_populates="hotel")
    rooms = relationship("Room", back_populates="hotel")


class Room(Base):
    __tablename__ ="rooms"

    id = Column(Integer, primary_key=True, index =True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_number = Column(String(50), nullable=False)
    room_type = Column(String(50), nullable=False)
    base_price = Column(Float, nullable = False)
    max_occupancy = Column(Integer , nullable=False)
    is_available = Column(Boolean, default=True)


    #Relationships
    hotel = relationship("Hotel", back_populates="rooms")
    booking = relationship("Bookings", back_populates="room")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)

    #booking details
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    guest_name = Column(String(200))
    guest_email = Column(String(200))
    num_guests = Column(Integer, nullable= False)

    booking_price = Column(Float, nullable = False)
    base_price = Column(Float, nullable=False)

    #MEtadata
    booking_date = Column(DateTime, default=datetime.utcnow)
    booking_source = Column(String(100))  # website, OTA, direct
    status = Column(String(50), default="confirmed")

    hotel = relationship("Hotel", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")


class DailyMetrics(Base):
    """Aggregated daily metrics for analytics"""

    __tablename__ = "daily_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    #Occupancy metrics
    occupancy_rate = Column(Float)  # Percentage
    rooms_occupied = Column(Integer)
    rooms_available = Column(Integer)
    
    # Revenue metrics
    total_revenue = Column(Float)
    average_daily_rate = Column(Float)  # ADR
    revenue_per_available_room = Column(Float)  # RevPAR
    
    # Demand indicators
    booking_count = Column(Integer, default=0)
    cancellation_count = Column(Integer, default=0)
    
    # Calculated at
    calculated_at = Column(DateTime, default=datetime.utcnow)