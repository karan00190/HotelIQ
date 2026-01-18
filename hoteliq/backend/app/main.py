from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.init_db import init_database
from app.database.connection import get_db
from app.services.data_generator import generate_all_data

# Import routers
from app.api import hotels, rooms, bookings, analytics, ingestion
from app.api import smart_queries, forecasting  # ← UPDATED (removed ai_chat)

import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="HotelIQ Revenue Management API",
    description="AI-powered revenue management platform with FREE open-source AI (no API costs!)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on app startup"""
    init_database()
    
    # Generate sample data (only once)
    db = next(get_db())
    try:
        generate_all_data(db)
    except Exception as e:
        print(f"Data generation skipped or failed: {e}")
    finally:
        db.close()

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "HotelIQ Revenue Management API",
        "status": "active",
        "version": "1.0.0",
        "features": {
            "data_pipeline": "ETL with 50+ feature engineering",
            "analytics": "Revenue metrics (ADR, RevPAR, Occupancy)",
            "smart_queries": "Pre-built analytical queries (NO AI COST)",
            "forecasting": "Prophet-based demand prediction (FREE)"
        },
        "cost": " FREE - No API costs!",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_cost": "FREE (open-source only)"
    }

# Include routers
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(analytics.router)
app.include_router(ingestion.router)
app.include_router(smart_queries.router)    #  FREE queries
app.include_router(forecasting.router)      #  FREE forecasting

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)