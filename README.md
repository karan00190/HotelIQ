
# 🏨 HotelIQ

**AI-Powered Revenue Management Platform for the Hospitality Industry**

**Project Status:**
**Backend Complete (80%) | Frontend In Progress | Deployment Pending**

---

## Overview

**HotelIQ** is an end-to-end revenue management platform designed to help hotels optimize pricing and forecast demand using data engineering and AI-driven intelligence.

The system automates data ingestion, validation, analytics, demand forecasting, and dynamic pricing recommendations—enabling hotels to move away from manual, intuition-based pricing decisions.

---

## Problem Statement

Hotels commonly struggle with:

* Manual pricing decisions without demand insights
* Data scattered across multiple booking channels
* Complex and error-prone revenue metric calculations
* Inability to predict future occupancy patterns

---

## Solution

HotelIQ provides an automated, intelligent platform that:

* Ingests booking data from multiple sources
* Validates and processes data via a robust ETL pipeline
* Generates 50+ machine-learning features
* Forecasts occupancy up to **30 days ahead**
* Recommends **optimal pricing** based on demand signals

---

## Key Features

---

### Data Pipeline

* Multi-source ingestion

  * CSV uploads
  * REST APIs
  * Database ingestion
* **9-layer validation framework**

  * Schema validation
  * Data types
  * Business rules
  * Duplicate detection
  * Outlier detection
* Automated data cleaning & standardization
* Batch processing (100 records per batch) with transaction management
* Idempotent operations to prevent duplicate records

---

### Feature Engineering

* **50+ features generated from 8 raw columns**
* **Time-based features (12)**

  * `day_of_week`, `season`, `is_weekend`, `is_peak_season`
* **Stay features (4)**

  * `length_of_stay`, `lead_time_days`
* **Pricing features (3)**

  * `price_per_night`, `discount_pct`
* **Aggregated features (8)**

  * 7-day & 30-day rolling averages
* **Occupancy features (2)**

  * `hotel_capacity`, `occupancy_rate`

---

### Analytics

* Core revenue metrics:

  * **ADR** (Average Daily Rate)
  * **RevPAR** (Revenue Per Available Room)
* Occupancy statistics with historical trends
* Pre-computed daily metrics for fast queries

  * ⏱️ Sub-200ms response times
* **7 pre-built smart analytical queries**, including:

  * Revenue analysis
  * Occupancy statistics
  * Booking source performance
  * Weekend vs weekday analysis
  * Cancellations
  * Popular room types

---

### Demand Forecasting

* **Prophet-based time-series forecasting**
* 30-day occupancy predictions
* Confidence intervals for forecast reliability
* Automated seasonality detection:

  * Daily
  * Weekly
  * Yearly patterns
* Trained on **180 days of historical data**

---

### Dynamic Pricing Engine

* Rule-based pricing engine analyzing **6 demand factors**
* Pricing factors include:

  * Predicted demand
  * Current occupancy
  * Weekend vs weekday
  * Seasonal trends
  * Booking lead time
  * Market pressure
* Pricing recommendations range from:

  * **30% discount** → **50% premium**
* Detailed explanations provided for every pricing decision

---

## System Architecture

### 🔗 Data Flow

**Data Sources → Ingestion → Validation → Cleaning → Feature Engineering → Database → Analytics → AI Layer → API Endpoints**

---

###  Three-Layer Architecture

#### 1️ Process Layer (Data Engineering)

* ETL pipeline with multi-stage validation
* Automated data cleaning
* Feature engineering for ML-ready datasets
* Batch processing with error handling

#### 2️ Analytics Layer (Business Intelligence)

* Pre-computed revenue metrics
* Daily KPI aggregation
* Optimized analytical queries

#### 3️ AI Layer (Intelligence)

* Prophet forecasting model
* Dynamic pricing recommendation engine
* 7 pre-built intelligent query endpoints

---

##  Tech Stack

### Backend

* **Python 3.10+**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **Pandas** (data processing)
* **Prophet** (forecasting)
* **SQLite** (development)
* **PostgreSQL** (planned production)

---

### Frontend (In Progress)

* **Next.js 14**
* **TypeScript**
* **Tailwind CSS**
* **Recharts** (data visualizations)
* **shadcn/ui** (component library)

---

### Deployment (Planned)

* Docker containerization
* AWS deployment:

  * EC2
  * RDS
  * S3
* CI/CD with GitHub Actions
* Redis caching
* Alembic database migrations

---

##  Database Schema

### Core Entities

* **Hotels**

  * Property details, location, capacity, star rating
* **Rooms**

  * Room type, pricing, occupancy limits
* **Bookings**

  * Guest details, dates, pricing, booking status
* **DailyMetrics**

  * Pre-aggregated KPIs:

    * Occupancy
    * Revenue
    * ADR
    * RevPAR

### Relationships

* Hotels → Rooms → Bookings
* Hotels → DailyMetrics

---

##  Project Status

*  Backend architecture & core logic complete (~80%)
*  Frontend dashboard under development
*  Deployment & CI/CD pending

---

If you want next:

* A **shorter “portfolio version” README**
* A **startup-style pitch README**
* Badges (Python, FastAPI, Docker, AWS)
* Architecture diagram (ASCII or image)

Say the word — this is already strong, we can polish it further.
