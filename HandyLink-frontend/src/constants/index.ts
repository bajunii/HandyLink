// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/users/login/',
  REGISTER: '/users/register/',
  VERIFY_EMAIL: '/users/verify-email/',
  REFRESH_TOKEN: '/users/refresh-token/',
  FORGOT_PASSWORD: '/users/forgot-password/',
  RESET_PASSWORD: '/users/reset-password/',
  
  // Users
  PROFILE: '/users/profile/',
  UPDATE_PROFILE: '/users/profile/update/',
  
  // Jobs
  JOBS: '/jobs/',
  CREATE_JOB: '/jobs/',
  JOB_DETAILS: (id: string) => `/jobs/${id}/`,
  JOB_APPLICATIONS: (jobId: string) => `/jobs/${jobId}/applications/`,
  APPLY_JOB: '/jobs/apply/',
  
  // Providers
  PROVIDERS: '/providers/',
  PROVIDER_DETAILS: (id: string) => `/providers/${id}/`,
  BECOME_PROVIDER: '/providers/register/',
  
  // Payments
  PAYMENTS: '/payments/',
  PROCESS_PAYMENT: '/payments/process/',
  PAYMENT_HISTORY: '/payments/history/',
  
  // Reviews
  REVIEWS: '/reviews/',
  CREATE_REVIEW: '/reviews/',
  
  // Notifications
  NOTIFICATIONS: '/notifications/',
  MARK_READ: (id: string) => `/notifications/${id}/mark-read/`,
};

// Colors
export const COLORS = {
  primary: '#2563eb',
  secondary: '#059669',
  error: '#dc2626',
  warning: '#d97706',
  success: '#059669',
  info: '#0ea5e9',
  
  // Neutral colors
  white: '#ffffff',
  black: '#000000',
  gray50: '#f9fafb',
  gray100: '#f3f4f6',
  gray200: '#e5e7eb',
  gray300: '#d1d5db',
  gray400: '#9ca3af',
  gray500: '#6b7280',
  gray600: '#4b5563',
  gray700: '#374151',
  gray800: '#1f2937',
  gray900: '#111827',
  
  // Background colors
  background: '#f8f9fa',
  surface: '#ffffff',
  card: '#ffffff',
};

// Typography
export const FONTS = {
  regular: 'System',
  medium: 'System',
  bold: 'System',
  light: 'System',
};

export const FONT_SIZES = {
  xs: 12,
  sm: 14,
  md: 16,
  lg: 18,
  xl: 20,
  '2xl': 24,
  '3xl': 30,
  '4xl': 36,
};

// Spacing
export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 40,
  '3xl': 48,
};

// Border Radius
export const BORDER_RADIUS = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

// Job Categories
export const JOB_CATEGORIES = [
  'Plumbing',
  'Electrical',
  'Cleaning',
  'Gardening',
  'Carpentry',
  'Painting',
  'Moving',
  'Tutoring',
  'Pet Care',
  'Home Repair',
  'Photography',
  'Web Development',
  'Graphic Design',
  'Other',
];

// Job Status
export const JOB_STATUS = {
  OPEN: 'open',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
} as const;

// Application Status
export const APPLICATION_STATUS = {
  PENDING: 'pending',
  ACCEPTED: 'accepted',
  REJECTED: 'rejected',
} as const;

// Payment Status
export const PAYMENT_STATUS = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed',
  REFUNDED: 'refunded',
} as const;

// Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'handylink_auth_token',
  REFRESH_TOKEN: 'handylink_refresh_token',
  USER_DATA: 'handylink_user_data',
  ONBOARDING_COMPLETED: 'handylink_onboarding_completed',
  THEME_PREFERENCE: 'handylink_theme_preference',
};

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
};

// App Configuration
export const APP_CONFIG = {
  NAME: process.env.EXPO_PUBLIC_APP_NAME || 'HandyLink',
  VERSION: process.env.EXPO_PUBLIC_APP_VERSION || '1.0.0',
  ENVIRONMENT: process.env.EXPO_PUBLIC_ENVIRONMENT || 'development',
  
  // File upload limits
  MAX_FILE_SIZE: parseInt(process.env.EXPO_PUBLIC_MAX_FILE_SIZE || '10485760'), // 10MB
  ALLOWED_FILE_TYPES: (process.env.EXPO_PUBLIC_ALLOWED_FILE_TYPES || 'jpg,jpeg,png,pdf').split(','),
  
  // Features flags
  FEATURES: {
    PUSH_NOTIFICATIONS: true,
    LOCATION_SERVICES: true,
    PAYMENT_INTEGRATION: true,
    MESSAGING: true,
    REVIEWS: true,
  },
};

// Validation Rules
export const VALIDATION_RULES = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^\+?[\d\s-()]+$/,
  PASSWORD_MIN_LENGTH: 8,
  OTP_LENGTH: 6,
  
  // Job validation
  TITLE_MIN_LENGTH: 10,
  TITLE_MAX_LENGTH: 100,
  DESCRIPTION_MIN_LENGTH: 20,
  DESCRIPTION_MAX_LENGTH: 1000,
  MIN_BUDGET: 10,
  MAX_BUDGET: 10000,
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  INVALID_CREDENTIALS: 'Invalid email or password.',
  EMAIL_REQUIRED: 'Email is required.',
  PASSWORD_REQUIRED: 'Password is required.',
  PASSWORD_TOO_SHORT: `Password must be at least ${VALIDATION_RULES.PASSWORD_MIN_LENGTH} characters.`,
  INVALID_EMAIL: 'Please enter a valid email address.',
  PASSWORDS_DONT_MATCH: 'Passwords do not match.',
  INVALID_OTP: 'Invalid verification code.',
  EXPIRED_OTP: 'Verification code has expired.',
  GENERIC_ERROR: 'Something went wrong. Please try again.',
};

// Success Messages
export const SUCCESS_MESSAGES = {
  REGISTRATION_SUCCESS: 'Registration successful! Please verify your email.',
  LOGIN_SUCCESS: 'Welcome back!',
  EMAIL_VERIFIED: 'Email verified successfully!',
  PROFILE_UPDATED: 'Profile updated successfully!',
  JOB_CREATED: 'Job posted successfully!',
  APPLICATION_SENT: 'Application sent successfully!',
  PAYMENT_SUCCESS: 'Payment completed successfully!',
  REVIEW_SUBMITTED: 'Review submitted successfully!',
};
