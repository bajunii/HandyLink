# HandyLink

## Project Overview

HandyLink is a hyper-local service marketplace that connects residents with trusted professionals in their area. Unlike generic platforms, HandyLink prioritizes verified providers, transparent pricing, and community-driven reviews to ensure reliability and quality.

## Features

### Provider Profiles
- Verified professionals create detailed profiles with skills, certifications, and work samples.
- Dynamic pricing (hourly, fixed-rate, or project-based).
- Real-time availability calendar for bookings.

### Customer Requests & Matching
- Users can post job requests (e.g., "Need a plumber for a leaky faucet") or browse providers.
- Smart matching based on proximity, ratings, and service type.
- Instant quotes from multiple providers for competitive pricing.

### Reviews & Trust System
- Verified customer reviews with photo/video proof of work.
- Provider badges (e.g., "Top Rated," "Fast Responder," "Community Favorite").
- Reporting system for accountability.

### Secure Payments
- In-app payments (escrow system for safety).
- Multiple options: credit card, digital wallets, or cash (if preferred).

### Monetization
- Commission fee (5-10% per transaction).

### Additional Features
- Urgent Service Requests – Priority listings for last-minute needs.
- Membership Perks – Discounts for frequent users or referrals.
- Local Business Spotlight – Promotes small businesses in the community.

---

## Directory Structure

### Backend (Python-Django, PostgreSQL)
```
backend/
├── HandyLink/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── apps/
│   │   ├── users/
│   │   ├── providers/
│   │   ├── jobs/
│   │   ├── reviews/
│   │   ├── payments/
│   │   └── ...
│   ├── manage.py
│   └── db.sqlite3 (for development; use PostgreSQL in production)
├── requirements.txt
└── README.md
```

### Frontend (React.js)
```
frontend/
├── public/
│   ├── index.html
│   └── ...
├── src/
│   ├── components/
│   │   ├── ProviderProfile/
│   │   ├── JobRequest/
│   │   ├── Review/
│   │   ├── Payment/
│   │   └── ...
│   ├── pages/
│   │   ├── Home/
│   │   ├── Providers/
│   │   ├── Jobs/
│   │   ├── Reviews/
│   │   └── ...
│   ├── App.js
│   ├── index.js
│   └── ...
├── package.json
└── README.md
```

---

## Database

- **Development:** SQLite (default Django setting)
- **Production:** PostgreSQL

---

## Getting Started

### Backend
1. Install dependencies: `pip install -r requirements.txt`
2. Configure PostgreSQL in `settings.py` for production.
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

### Frontend
1. Install dependencies: `npm install`
2. Start development server: `npm start`

---

##
