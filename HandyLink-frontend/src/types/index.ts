// User Types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  is_verified: boolean;
  is_provider: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  password2: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  is_provider?: boolean;
}

export interface VerificationData {
  email: string;
  otp: string;
}

// Provider Types
export interface Provider {
  id: string;
  user: User;
  bio: string;
  skills: string[];
  location: string;
  hourly_rate: number;
  rating: number;
  total_reviews: number;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

// Job Types
export interface Job {
  id: string;
  title: string;
  description: string;
  category: string;
  location: string;
  budget: number;
  status: 'open' | 'in_progress' | 'completed' | 'cancelled';
  customer: User;
  provider?: Provider;
  created_at: string;
  updated_at: string;
  deadline?: string;
}

export interface JobApplication {
  id: string;
  job: string;
  provider: Provider;
  status: 'pending' | 'accepted' | 'rejected';
  proposed_price: number;
  message: string;
  created_at: string;
}

// Payment Types
export interface Payment {
  id: string;
  job: string;
  amount: number;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  payment_method: 'stripe' | 'paypal';
  transaction_id?: string;
  created_at: string;
}

// Review Types
export interface Review {
  id: string;
  job: string;
  reviewer: User;
  reviewee: User;
  rating: number;
  comment: string;
  created_at: string;
}

// Notification Types
export interface Notification {
  id: string;
  user: string;
  title: string;
  message: string;
  type: 'job_application' | 'job_update' | 'payment' | 'review' | 'general';
  is_read: boolean;
  created_at: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Navigation Types
export type RootStackParamList = {
  Splash: undefined;
  Auth: undefined;
  Main: undefined;
  Login: undefined;
  Register: undefined;
  VerifyEmail: { email: string };
  ForgotPassword: undefined;
  Home: undefined;
  JobDetails: { jobId: string };
  CreateJob: undefined;
  Profile: { userId?: string };
  Messages: undefined;
  Notifications: undefined;
  Settings: undefined;
};
