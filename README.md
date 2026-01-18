HotelIQ - AI-Powered Revenue Management Platform
End-to-end revenue management system for hospitality industry with demand forecasting and dynamic pricing optimization.

Project Status: Backend Complete (80%) | Frontend In Progress | Deployment Pending

OverviewHotelIQ is a revenue management platform designed for hotels to optimize pricing and forecast demand. The system automates data processing, calculates key performance metrics, and provides AI-driven pricing recommendations.Problem StatementHotels struggle with:

Manual pricing decisions without demand insights
Data scattered across multiple booking channels
Complex revenue metric calculations
Inability to predict future occupancy patterns
SolutionAn automated platform that:

Ingests booking data from multiple sources
Validates and processes data through ETL pipeline
Generates 50+ ML features for predictive modeling
Forecasts occupancy 30 days ahead
Recommends optimal pricing based on demand
Key FeaturesData Pipeline

Multi-source ingestion (CSV upload, REST API, database)
9-layer validation framework (schema, types, business rules, duplicates, outliers)
Automated data cleaning and standardization
Batch processing with transaction management (100 records per batch)
Idempotent operations preventing duplicates
Feature Engineering

50+ features generated from 8 raw columns
Time features: day_of_week, season, is_weekend, is_peak_season (12 features)
Stay features: length_of_stay, lead_time_days (4 features)
Pricing features: price_per_night, discount_pct (3 features)
Aggregated features: 7-day/30-day rolling averages (8 features)
Occupancy features: hotel capacity, occupancy_rate (2 features)
Analytics

Revenue metrics: ADR (Average Daily Rate), RevPAR (Revenue Per Available Room)
Occupancy statistics with historical trends
Pre-computed daily metrics for fast queries (sub-200ms response)
7 pre-built smart queries: revenue analysis, occupancy stats, booking sources, weekend vs weekday, cancellations, popular rooms
Demand Forecasting

Prophet-based time-series model
30-day occupancy predictions with confidence intervals
Automated seasonality detection (daily, weekly, yearly patterns)
Trained on 180 days of historical data
Dynamic Pricing

Rule-based pricing engine analyzing 6 factors
Factors: predicted demand, current occupancy, weekend/weekday, season, lead time, market pressure
Price recommendations ranging from 30% discount to 50% premium
Detailed explanations for each pricing decision
ArchitectureSystem LayersData Sources → Ingestion Layer → Validation Layer → Cleaning Layer → Feature Engineering → Database → Analytics Layer → AI Layer → API EndpointsThree-Layer DesignProcess Layer (Data Engineering)

ETL pipeline with validation and cleaning
Feature engineering generating ML-ready data
Batch processing with error handling
Analytics Layer (Business Intelligence)

Pre-computed revenue metrics
Smart analytical queries
Daily metrics aggregation
AI Layer (Intelligence)

Prophet forecasting model
Dynamic pricing recommendations
7 pre-built query endpoints
Tech StackBackend

Python 3.10+, FastAPI, SQLAlchemy, Pydantic
Pandas (data processing), Prophet (forecasting)
SQLite (development), PostgreSQL (planned production)
In Progress

Next.js 14, TypeScript, Tailwind CSS
Recharts (visualizations), shadcn/ui (components)
Planned

Docker containerization
AWS deployment (EC2, RDS, S3)
CI/CD with GitHub Actions
Redis caching, Alembic migrations
Database SchemaHotels: Properties with location, capacity, star rating
Rooms: Individual rooms with type, pricing, occupancy limits
Bookings: Reservations with guest details, dates, pricing, status
DailyMetrics: Pre-aggregated KPIs (occupancy, revenue, ADR, RevPAR)Relations: Hotels → Rooms → Bookings, Hotels → DailyMetrics
