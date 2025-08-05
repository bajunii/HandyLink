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

## Technology Stack

### Backend
- **Framework:** Django 4.2.10 + Django REST Framework
- **Language:** Python 3.13+
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT (JSON Web Tokens)
- **Email:** SMTP with HTML templates
- **API Documentation:** Swagger/OpenAPI

### Frontend
- **Framework:** React Native with Expo
- **Language:** TypeScript/JavaScript
- **State Management:** Context API / Redux (planned)
- **Navigation:** React Navigation
- **UI Components:** Custom component library
- **Platform:** iOS & Android

---

## Directory Structure

```
HandyLink/
├── HandyLink-backend/          # Django REST API
│   ├── core/                   # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/                   # Django applications
│   │   ├── users/              # User management & authentication
│   │   ├── providers/          # Service provider profiles
│   │   ├── jobs/               # Job postings & applications
│   │   ├── reviews/            # Rating & review system
│   │   ├── payments/           # Payment processing
│   │   └── notifications/      # Email & push notifications
│   ├── templates/              # Email templates
│   ├── media/                  # User uploads
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
├── HandyLink-frontend/         # React Native Mobile App
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── common/         # Button, Input, Loading, etc.
│   │   │   └── forms/          # Form components
│   │   ├── screens/            # App screens
│   │   │   ├── auth/           # Login, Register, etc.
│   │   │   ├── jobs/           # Job browsing, posting
│   │   │   ├── profile/        # User profiles
│   │   │   └── dashboard/      # Main app screens
│   │   ├── services/           # API integration
│   │   ├── utils/              # Helper functions
│   │   ├── types/              # TypeScript type definitions
│   │   └── constants/          # App constants
│   ├── assets/                 # Images, fonts, etc.
│   ├── App.tsx                 # Main app component
│   ├── package.json
│   └── README.md
│
└── README.md                   # This file
```

---

## Database Schema

### Core Models
- **Users:** Authentication, profiles, permissions
- **Providers:** Service provider details, skills, availability
- **Jobs:** Job postings, applications, status tracking
- **Reviews:** Ratings, comments, photo evidence
- **Payments:** Transaction records, escrow system
- **Notifications:** Email & push notification logs

---

## API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/verify-email/` - Email verification
- `POST /api/users/logout/` - User logout

### Jobs & Services
- `GET /api/jobs/` - List jobs
- `POST /api/jobs/` - Create job posting
- `GET /api/jobs/{id}/` - Job details
- `POST /api/jobs/{id}/apply/` - Apply to job

### Providers
- `GET /api/providers/` - List providers
- `POST /api/providers/` - Register as provider
- `GET /api/providers/{id}/` - Provider profile

### Reviews & Ratings
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Submit review
- `GET /api/reviews/stats/` - Review statistics

---

## Getting Started

### Prerequisites
- **Backend:** Python 3.13+, pip, virtualenv
- **Frontend:** Node.js 18+, npm/yarn, Expo CLI
- **Mobile:** Expo Go app (for testing)

### Backend Setup
```bash
cd HandyLink-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Edit with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
cd HandyLink-frontend

# Install dependencies
npm install

# Start development server
npx expo start

# On your phone:
# 1. Install Expo Go from App Store/Play Store
# 2. Scan the QR code displayed in terminal
```

---

## Development Status

### ✅ Completed Features
- **Backend API:** Complete REST API with all endpoints
- **Authentication:** JWT-based auth with email verification
- **Database Models:** All core models implemented
- **Admin Interface:** Django admin for management
- **Email System:** HTML email templates with notifications
- **API Documentation:** Swagger/OpenAPI integration
- **Frontend Foundation:** React Native app structure
- **Registration Screen:** User registration with validation

### 🚧 In Progress
- **Mobile UI:** Core screens and navigation
- **API Integration:** Connecting frontend to backend
- **Payment System:** Stripe/PayPal integration

### 📋 Planned Features
- **Real-time Chat:** Provider-customer messaging
- **Push Notifications:** Job alerts and updates
- **Map Integration:** Location-based provider search
- **Photo Upload:** Job documentation and reviews
- **Advanced Search:** Filters and sorting options

---

## Deployment

### Backend (Production)
- **Hosting:** Railway, Heroku, or DigitalOcean
- **Database:** PostgreSQL
- **Static Files:** AWS S3 or Cloudinary
- **Email:** SendGrid or Mailgun

### Frontend (Production)
- **iOS:** App Store via Expo Application Services (EAS)
- **Android:** Google Play Store via EAS
- **Updates:** Over-the-air updates with Expo

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Contact & Support

- **Developer:** Your Development Team
- **Email:** support@handylink.com
- **Documentation:** [API Docs](http://localhost:8000/swagger/)
- **Issues:** GitHub Issues section

---

## Acknowledgments

- Django REST Framework for robust API development
- React Native & Expo for cross-platform mobile development
- Community contributors and testers

---

*HandyLink - Connecting communities with trusted local services* 🔧📱

