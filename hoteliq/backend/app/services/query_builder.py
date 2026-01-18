from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
from app.models.hotel import Booking, Hotel, Room, DailyMetrics

class QueryBuilder:
    def __init__(self, db:Session):
        self.db = db

    def get_total_revenue(
            self, 
            hotel_id: Optional[int] = None,
            start_date: Optional[date] = None,
            end_date: Optional[date] =None
    ) -> Dict:
        query = self.db.query(
            func.sum(Booking.booking_price).label('total_revenue'),
            func.count(Booking.id).label('booking_count')

        ).filter(Booking.status.in_(['confirmed', 'completed']))

        if hotel_id:
            query = query.filter(Booking.hotel_id == hotel_id)
        if start_date:
            query = query.filter(Booking.check_in_date >= start_date)

        if end_date: 
            query = query.filter(Booking.check_out_date <= end_date)
        
        result = query.first()


        return{
            "total_revenue": float(result.total_revenue or 0),
            "booking_count": result.booking_count or 0,
            "filters": {
                "hotel_id": hotel_id,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
    def get_occupancy_stats(
        self,
        hotel_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict:
        """Get occupancy statistics"""
        query = self.db.query(DailyMetrics).filter(DailyMetrics.hotel_id == hotel_id)
        
        if start_date:
            query = query.filter(DailyMetrics.date >= start_date)
        if end_date:
            query = query.filter(DailyMetrics.date <= end_date)
        
        metrics = query.all()
        
        if not metrics:
            return {"error": "No data found for specified filters"}
        
        occupancy_rates = [m.occupancy_rate for m in metrics if m.occupancy_rate]
        
        return {
            "hotel_id": hotel_id,
            "days_analyzed": len(metrics),
            "average_occupancy": round(sum(occupancy_rates) / len(occupancy_rates), 2) if occupancy_rates else 0,
            "max_occupancy": round(max(occupancy_rates), 2) if occupancy_rates else 0,
            "min_occupancy": round(min(occupancy_rates), 2) if occupancy_rates else 0,
            "date_range": {
                "start": metrics[0].date.isoformat(),
                "end": metrics[-1].date.isoformat()
            }
        }
    
    def get_top_bookings(
        self,
        limit: int = 10,
        order_by: str = "price"  # 'price' or 'date'
    ) -> List[Dict]:
        """Get top bookings by price or most recent"""
        query = self.db.query(Booking)
        
        if order_by == "price":
            query = query.order_by(Booking.booking_price.desc())
        else:
            query = query.order_by(Booking.check_in_date.desc())
        
        bookings = query.limit(limit).all()
        
        return [
            {
                "id": b.id,
                "hotel_id": b.hotel_id,
                "guest_name": b.guest_name,
                "check_in_date": b.check_in_date.isoformat(),
                "check_out_date": b.check_out_date.isoformat(),
                "booking_price": b.booking_price,
                "status": b.status
            }
            for b in bookings
        ]
    
    def get_booking_source_distribution(self, hotel_id: Optional[int] = None) -> Dict:
        """Where do bookings come from?"""
        query = self.db.query(
            Booking.booking_source,
            func.count(Booking.id).label('count'),
            func.sum(Booking.booking_price).label('revenue')
        ).group_by(Booking.booking_source)
        
        if hotel_id:
            query = query.filter(Booking.hotel_id == hotel_id)
        
        results = query.all()
        
        distribution = []
        total_bookings = sum(r.count for r in results)
        
        for r in results:
            distribution.append({
                "source": r.booking_source,
                "booking_count": r.count,
                "percentage": round((r.count / total_bookings * 100), 2) if total_bookings > 0 else 0,
                "total_revenue": float(r.revenue or 0)
            })
        
        return {
            "distribution": sorted(distribution, key=lambda x: x['booking_count'], reverse=True),
            "total_bookings": total_bookings
        }
    
    def get_weekend_vs_weekday_comparison(self, hotel_id: int) -> Dict:
        """Compare weekend vs weekday performance"""
        bookings = self.db.query(Booking).filter(Booking.hotel_id == hotel_id).all()
        
        weekend_bookings = []
        weekday_bookings = []
        
        for b in bookings:
            if b.check_in_date.weekday() in [5, 6]:  # Saturday, Sunday
                weekend_bookings.append(b)
            else:
                weekday_bookings.append(b)
        
        weekend_revenue = sum(b.booking_price for b in weekend_bookings)
        weekday_revenue = sum(b.booking_price for b in weekday_bookings)
        
        return {
            "weekend": {
                "booking_count": len(weekend_bookings),
                "total_revenue": weekend_revenue,
                "average_price": weekend_revenue / len(weekend_bookings) if weekend_bookings else 0
            },
            "weekday": {
                "booking_count": len(weekday_bookings),
                "total_revenue": weekday_revenue,
                "average_price": weekday_revenue / len(weekday_bookings) if weekday_bookings else 0
            },
            "weekend_premium_percent": round(
                ((weekend_revenue / len(weekend_bookings)) / (weekday_revenue / len(weekday_bookings)) - 1) * 100, 2
            ) if weekend_bookings and weekday_bookings else 0
        }
    
    def get_cancellation_analysis(self, hotel_id: Optional[int] = None) -> Dict:
        """Analyze cancellation patterns"""
        query = self.db.query(Booking)
        
        if hotel_id:
            query = query.filter(Booking.hotel_id == hotel_id)
        
        all_bookings = query.all()
        cancelled = [b for b in all_bookings if b.status == 'cancelled']
        
        total_bookings = len(all_bookings)
        cancelled_count = len(cancelled)
        cancellation_rate = (cancelled_count / total_bookings * 100) if total_bookings > 0 else 0
        
        lost_revenue = sum(b.booking_price for b in cancelled)
        
        return {
            "total_bookings": total_bookings,
            "cancelled_bookings": cancelled_count,
            "cancellation_rate": round(cancellation_rate, 2),
            "lost_revenue": lost_revenue
        }
    
    def get_popular_room_types(self, hotel_id: int, limit: int = 5) -> List[Dict]:
        """Most popular room types"""
        query = self.db.query(
            Room.room_type,
            func.count(Booking.id).label('booking_count'),
            func.avg(Booking.booking_price).label('avg_price')
        ).join(Booking, Room.id == Booking.room_id).filter(
            Room.hotel_id == hotel_id
        ).group_by(Room.room_type).order_by(func.count(Booking.id).desc()).limit(limit)
        
        results = query.all()
        
        return [
            {
                "room_type": r.room_type,
                "booking_count": r.booking_count,
                "average_price": round(float(r.avg_price), 2)
            }
            for r in results
        ]
    
    def get_available_queries(self) -> List[Dict]:
        """List all available pre-built queries"""
        return [
            {
                "id": "total_revenue",
                "name": "Total Revenue",
                "description": "Get total revenue and booking count with optional filters",
                "parameters": ["hotel_id (optional)", "start_date (optional)", "end_date (optional)"]
            },
            {
                "id": "occupancy_stats",
                "name": "Occupancy Statistics",
                "description": "Get average, min, max occupancy for a hotel",
                "parameters": ["hotel_id (required)", "start_date (optional)", "end_date (optional)"]
            },
            {
                "id": "top_bookings",
                "name": "Top Bookings",
                "description": "Get highest-priced or most recent bookings",
                "parameters": ["limit (optional, default 10)", "order_by (price/date)"]
            },
            {
                "id": "booking_source_distribution",
                "name": "Booking Source Distribution",
                "description": "Where do bookings come from? (website, OTA, direct, etc.)",
                "parameters": ["hotel_id (optional)"]
            },
            {
                "id": "weekend_vs_weekday",
                "name": "Weekend vs Weekday Comparison",
                "description": "Compare performance between weekends and weekdays",
                "parameters": ["hotel_id (required)"]
            },
            {
                "id": "cancellation_analysis",
                "name": "Cancellation Analysis",
                "description": "Analyze cancellation rate and lost revenue",
                "parameters": ["hotel_id (optional)"]
            },
            {
                "id": "popular_room_types",
                "name": "Popular Room Types",
                "description": "Most booked room types with average prices",
                "parameters": ["hotel_id (required)", "limit (optional, default 5)"]
            }
        ]