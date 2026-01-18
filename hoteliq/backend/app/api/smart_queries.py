from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import date
from typing import Optional
from app.database.connection import get_db
from app.services.query_builder import QueryBuilder

router = APIRouter(prefix="/smart-queries", tags =["Smart Queries (No AI Cost)"])

@router.get("/available")
def list_available_queries(db:Session = Depends(get_db)):

    builder = QueryBuilder(db)
    return{
        "queries": builder.get_available_queries(),
        "note": "These queries work without an AI costs"
    }

@router.get("/total_revenue")
def query_total_revenue(
    hotel_id: Optional[int] = None,
    start_date: Optional[date]= None,
    end_date: Optional[date] =None, 
    db: Session = Depends(get_db)
):
    builder = QueryBuilder(db)
    return builder.get_total_revenue(hotel_id,start_date, end_date)

@router.get("/occupancy-stats/{hotel_id}")
def query_occupancy_stats(
    hotel_id: int, 
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db:Session = Depends(get_db)
):
    builder = QueryBuilder(db)
    return builder.get_occupancy_stats(hotel_id, start_date, end_date)

@router.get("/top_bookings")
def query_top_bookings(
    limit: int = Query(10, ge =1, le =50),
    order_by:str = Query("price", regex="^(price|date)$"),
    db:Session = Depends(get_db)
):
    builder = QueryBuilder(db)
    return builder.get_top_bookings(limit, order_by)

@router.get("/booking-sources")
def query_booking_sources(
    hotel_id: Optional[int] =None,
    db:Session = Depends(get_db)
):
    builder = QueryBuilder(db)
    return builder.get_booking_source_distribution(hotel_id)


@router.get("/weekend-vs-weekday/{hotel_id}")
def query_weekend_weekday(
    hotel_id: int,
    db: Session = Depends(get_db)
):
    """
    Question: "How do weekends compare to weekdays?"
    
    """
    builder = QueryBuilder(db)
    return builder.get_weekend_vs_weekday_comparison(hotel_id)


@router.get("/cancellations")
def query_cancellations(
    hotel_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Question: "What is my cancellation rate?"
    
    """
    builder = QueryBuilder(db)
    return builder.get_cancellation_analysis(hotel_id)


@router.get("/popular-rooms/{hotel_id}")
def query_popular_rooms(
    hotel_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Question: "Which room types are most popular?"
    
    """
    builder = QueryBuilder(db)
    return builder.get_popular_room_types(hotel_id, limit)
