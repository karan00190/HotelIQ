from app.database.connection import engine,Base
from app.models.hotel import Hotel, Room, Booking ,DailyMetrics

def init_database():

    print("Creating database tables..")
    Base.metadata.create_all(bind= engine)
    print("Database tables created successfullyy")

if __name__ == "__main__":
    init_database()