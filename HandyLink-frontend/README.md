# 📱 HandyLink Mobile App - React Native Frontend

<div align="center">
  <h3>🔧 Your Trusted Service Marketplace</h3>
  <p>Connecting customers with skilled service providers</p>
  
  [![React Native](https://img.shields.io/badge/React%20Native-0.72+-61DAFB?style=for-the-badge&logo=react)](https://reactnative.dev/)
  [![Expo](https://img.shields.io/badge/Expo-49+-000020?style=for-the-badge&logo=expo)](https://expo.dev/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
</div>

---

## 🚀 Project Overview

HandyLink is a comprehensive mobile marketplace application built with React Native that connects customers with trusted service providers. The app features real-time messaging, payment processing, job management, and location-based services.

### 📋 Key Features
- 👤 **Dual User Types**: Customers & Service Providers
- 🔐 **Secure Authentication**: JWT-based with email verification
- 💼 **Job Management**: Post, browse, apply, and manage jobs
- 💬 **Real-time Messaging**: In-app communication system
- 💳 **Payment Integration**: Secure payments with Stripe/PayPal
- ⭐ **Reviews & Ratings**: Comprehensive feedback system
- 📍 **Location Services**: GPS-based provider discovery
- 🔔 **Push Notifications**: Real-time updates and alerts
- 📷 **Photo Upload**: Job documentation and portfolio images

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

| Software | Version | Download Link | Purpose |
|----------|---------|---------------|---------|
| **Node.js** | 18.0+ | [nodejs.org](https://nodejs.org/) | JavaScript runtime |
| **npm/yarn** | Latest | Included with Node.js | Package manager |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) | Version control |
| **Android Studio** | Latest | [developer.android.com](https://developer.android.com/studio) | Android development |
| **Xcode** | Latest | Mac App Store | iOS development (Mac only) |

### Development Tools

```bash
# Install Expo CLI globally
npm install -g @expo/cli

# Install React Native CLI (optional, for bare workflow)
npm install -g react-native-cli

# Install TypeScript globally (recommended)
npm install -g typescript
```

### Mobile Development Setup

#### Android Setup
1. **Install Android Studio**
2. **Configure Android SDK**:
   - SDK Platforms: Android 13 (API 33)
   - SDK Tools: Android SDK Build-Tools, Android Emulator
3. **Set Environment Variables**:
   ```bash
   ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
   ```
4. **Add to PATH**:
   ```bash
   %ANDROID_HOME%\platform-tools
   %ANDROID_HOME%\tools
   ```

#### iOS Setup (Mac Only)
1. **Install Xcode** from Mac App Store
2. **Install Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```
3. **Install iOS Simulator**
4. **Install CocoaPods**:
   ```bash
   sudo gem install cocoapods
   ```

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/handylink.git
cd handylink/HandyLink-frontend
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### 3. Environment Configuration
Create a `.env` file in the root directory:

```env
# API Configuration
EXPO_PUBLIC_API_BASE_URL=http://localhost:8000/api
EXPO_PUBLIC_BACKEND_URL=http://localhost:8000

# App Configuration
EXPO_PUBLIC_APP_NAME=HandyLink
EXPO_PUBLIC_APP_VERSION=1.0.0
EXPO_PUBLIC_ENVIRONMENT=development

# Authentication
EXPO_PUBLIC_JWT_STORAGE_KEY=handylink_auth_token
EXPO_PUBLIC_REFRESH_TOKEN_KEY=handylink_refresh_token

# Google Services
EXPO_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
EXPO_PUBLIC_GOOGLE_PLACES_API_KEY=your_google_places_api_key

# Payment Gateways
EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
EXPO_PUBLIC_PAYPAL_CLIENT_ID=your_paypal_client_id

# Push Notifications
EXPO_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
EXPO_PUBLIC_FIREBASE_PROJECT_ID=your_firebase_project_id
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id

# Social Authentication
EXPO_PUBLIC_GOOGLE_OAUTH_CLIENT_ID=your_google_oauth_client_id
EXPO_PUBLIC_FACEBOOK_APP_ID=your_facebook_app_id

# File Upload
EXPO_PUBLIC_MAX_FILE_SIZE=10485760
EXPO_PUBLIC_ALLOWED_FILE_TYPES=jpg,jpeg,png,pdf,doc,docx

# Debug Settings
EXPO_PUBLIC_DEBUG_MODE=true
EXPO_PUBLIC_LOG_LEVEL=debug
```

### 4. Start Development Server
```bash
# Start Expo development server
npx expo start

# Or with specific options
npx expo start --clear    # Clear cache
npx expo start --offline  # Offline mode
npx expo start --tunnel   # Tunnel for external devices
```

---

## 🏗️ Project Structure

```
HandyLink-frontend/
├── 📁 src/
│   ├── 📁 components/          # Reusable UI components
│   │   ├── 📁 common/         # Common components (Button, Input, etc.)
│   │   ├── 📁 forms/          # Form components
│   │   ├── 📁 navigation/     # Navigation components
│   │   └── 📁 ui/             # UI-specific components
│   ├── 📁 screens/            # App screens
│   │   ├── 📁 auth/           # Authentication screens
│   │   ├── 📁 jobs/           # Job-related screens
│   │   ├── 📁 profile/        # Profile screens
│   │   ├── 📁 messaging/      # Chat screens
│   │   └── 📁 payments/       # Payment screens
│   ├── 📁 navigation/         # Navigation configuration
│   ├── 📁 services/           # API services
│   │   ├── 📁 api/            # API endpoints
│   │   ├── 📁 auth/           # Authentication services
│   │   └── 📁 storage/        # Local storage
│   ├── 📁 store/              # Redux store configuration
│   │   ├── 📁 slices/         # Redux slices
│   │   └── 📁 middleware/     # Custom middleware
│   ├── 📁 utils/              # Utility functions
│   ├── 📁 constants/          # App constants
│   ├── 📁 types/              # TypeScript type definitions
│   ├── 📁 hooks/              # Custom React hooks
│   └── 📁 assets/             # Images, fonts, etc.
├── 📁 __tests__/              # Test files
├── 📄 app.json               # Expo configuration
├── 📄 babel.config.js        # Babel configuration
├── 📄 metro.config.js        # Metro bundler configuration
├── 📄 tsconfig.json          # TypeScript configuration
├── 📄 package.json           # Dependencies
└── 📄 README.md              # This file
```

---

## 📚 Technology Stack

### Core Technologies
```json
{
  "react-native": "^0.72.0",
  "expo": "^49.0.0",
  "typescript": "^5.0.0",
  "react": "^18.2.0"
}
```

### Navigation
```json
{
  "@react-navigation/native": "^6.1.0",
  "@react-navigation/stack": "^6.3.0",
  "@react-navigation/bottom-tabs": "^6.5.0",
  "@react-navigation/drawer": "^6.6.0"
}
```

### State Management
```json
{
  "@reduxjs/toolkit": "^1.9.0",
  "react-redux": "^8.1.0",
  "@tanstack/react-query": "^4.29.0"
}
```

### UI Components
```json
{
  "react-native-elements": "^3.4.0",
  "react-native-vector-icons": "^10.0.0",
  "react-native-paper": "^5.8.0",
  "react-native-ui-lib": "^7.0.0"
}
```

### Backend Integration
```json
{
  "axios": "^1.4.0",
  "@react-native-async-storage/async-storage": "^1.19.0",
  "react-native-mmkv": "^2.10.0"
}
```

### Features & Services
```json
{
  "react-native-maps": "^1.7.0",
  "react-native-image-picker": "^5.6.0",
  "react-native-camera": "^4.2.0",
  "@react-native-firebase/app": "^18.0.0",
  "@react-native-firebase/messaging": "^18.0.0",
  "react-native-push-notification": "^8.1.0",
  "@stripe/stripe-react-native": "^0.28.0",
  "react-native-paypal": "^2.2.0",
  "react-native-geolocation-service": "^5.3.0",
  "react-native-permissions": "^3.8.0"
}
```

---

## 🚀 Development Scripts

### Available Commands

| Command | Description |
|---------|-------------|
| `npm start` | Start Expo development server |
| `npm run android` | Run on Android device/emulator |
| `npm run ios` | Run on iOS device/simulator |
| `npm run web` | Run on web browser |
| `npm run build` | Build for production |
| `npm run test` | Run test suite |
| `npm run test:watch` | Run tests in watch mode |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Fix ESLint issues |
| `npm run type-check` | Run TypeScript type checking |
| `npm run format` | Format code with Prettier |

### Development Workflow
```bash
# Start development
npm start

# In another terminal - for Android
npm run android

# In another terminal - for iOS (Mac only)
npm run ios

# Run tests
npm run test

# Type checking
npm run type-check
```

---

## 🔧 Configuration

### Expo Configuration (app.json)
```json
{
  "expo": {
    "name": "HandyLink",
    "slug": "handylink",
    "version": "1.0.0",
    "platforms": ["ios", "android"],
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "plugins": [
      "expo-font",
      "expo-location",
      "expo-camera",
      "expo-notifications"
    ]
  }
}
```

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "es2017",
    "lib": ["es2017", "dom"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  }
}
```

---

## 🏃‍♂️ Quick Start Guide

### 1. First Time Setup
```bash
# Clone and setup
git clone <repository-url>
cd HandyLink-frontend
npm install

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start development
npm start
```

### 2. Connect to Backend
Ensure your Django backend is running:
```bash
# In HandyLink-backend directory
python manage.py runserver
```

### 3. Test on Device
```bash
# Install Expo Go app on your phone
# Scan QR code from terminal
# Or run on emulator
npm run android  # or npm run ios
```

---

## 🧪 Testing

### Testing Setup
```bash
# Install testing dependencies
npm install --save-dev @testing-library/react-native @testing-library/jest-native
```

### Running Tests
```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- --testNamePattern="Login"
```

### Test Structure
```
__tests__/
├── components/
├── screens/
├── services/
├── utils/
└── setup.js
```

---

## 🚀 Deployment

### Development Build
```bash
# Create development build
npx expo build:android --type apk
npx expo build:ios --type simulator
```

### Production Build
```bash
# Build for app stores
npx expo build:android --type app-bundle
npx expo build:ios --type archive
```

### EAS Build (Recommended)
```bash
# Install EAS CLI
npm install -g @expo/eas-cli

# Configure EAS
eas build:configure

# Build for production
eas build --platform android
eas build --platform ios
```

---

## 🔗 API Integration

### Backend Endpoints
The app connects to the Django REST API with the following main endpoints:

```typescript
// Authentication
POST /api/users/register/
POST /api/users/login/
POST /api/users/verify-email/
POST /api/users/refresh-token/

// Jobs
GET /api/jobs/
POST /api/jobs/
GET /api/jobs/{id}/
PUT /api/jobs/{id}/
DELETE /api/jobs/{id}/

// Providers
GET /api/providers/
GET /api/providers/{id}/
POST /api/providers/applications/

// Payments
POST /api/payments/process/
GET /api/payments/history/

// Reviews
GET /api/reviews/
POST /api/reviews/

// Notifications
GET /api/notifications/
PUT /api/notifications/{id}/mark-read/
```

### API Service Example
```typescript
// src/services/api/auth.ts
export const authAPI = {
  login: (credentials: LoginCredentials) => 
    api.post('/users/login/', credentials),
  
  register: (userData: RegisterData) => 
    api.post('/users/register/', userData),
  
  verifyEmail: (data: VerificationData) => 
    api.post('/users/verify-email/', data),
};
```

---

## 🎨 UI/UX Guidelines

### Design System
- **Colors**: Blue (#2563eb), Green (#059669), Red (#dc2626)
- **Typography**: Inter font family
- **Spacing**: 4px base unit (8px, 12px, 16px, 24px, 32px)
- **Border Radius**: 8px standard, 12px cards, 24px buttons

### Component Library
```typescript
// Example component usage
import { Button, Input, Card } from '@/components/common';

<Button 
  variant="primary" 
  size="large" 
  onPress={handleSubmit}
>
  Submit Job
</Button>
```

---

## 🔧 Troubleshooting

### Common Issues

#### Metro Bundler Issues
```bash
# Clear cache
npx react-native start --reset-cache
# or
npm start -- --clear
```

#### Android Build Issues
```bash
# Clean build
cd android
./gradlew clean
cd ..
npm run android
```

#### iOS Build Issues
```bash
# Clean build (Mac only)
cd ios
xcodebuild clean
cd ..
npm run ios
```

#### Permission Issues
```bash
# Reset permissions
npx expo install expo-permissions
```

### Environment Issues
- Ensure backend is running on `http://localhost:8000`
- Check API endpoint URLs in `.env` file
- Verify all required environment variables are set

---

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow ESLint and Prettier configuration
2. **Commits**: Use conventional commit messages
3. **Testing**: Write tests for new features
4. **Documentation**: Update README for new features

### Pull Request Process
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'feat: add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

### Getting Help
- 📧 **Email**: support@handylink.com
- 💬 **Discord**: [HandyLink Community](https://discord.gg/handylink)
- 📚 **Documentation**: [docs.handylink.com](https://docs.handylink.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-repo/issues)

### Resources
- [React Native Documentation](https://reactnative.dev/docs/getting-started)
- [Expo Documentation](https://docs.expo.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)

---

<div align="center">
  <p>Built with ❤️ by the HandyLink Team</p>
  <p>🔧 <strong>Connecting Skills, Creating Opportunities</strong> 🔧</p>
</div>
