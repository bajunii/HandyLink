import apiService from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { 
  User, 
  AuthTokens, 
  LoginCredentials, 
  RegisterData, 
  VerificationData 
} from '../types/index';
import { API_ENDPOINTS, STORAGE_KEYS } from '@constants/index';

export class AuthService {
  // Login user
  async login(credentials: LoginCredentials): Promise<{ user: User; tokens: AuthTokens }> {
    try {
      const response = await apiService.post<{ user: User; tokens: AuthTokens }>(
        API_ENDPOINTS.LOGIN,
        credentials
      );

      // Store tokens
      await this.storeTokens(response.tokens);
      
      // Store user data
      await AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(response.user));

      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  // Register user
  async register(userData: RegisterData): Promise<{ message: string; user: User }> {
    try {
      const response = await apiService.post<{ message: string; user: User }>(
        API_ENDPOINTS.REGISTER,
        userData
      );

      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  // Verify email with OTP
  async verifyEmail(data: VerificationData): Promise<{ user: User; tokens: AuthTokens }> {
    try {
      const response = await apiService.post<{ user: User; tokens: AuthTokens }>(
        API_ENDPOINTS.VERIFY_EMAIL,
        data
      );

      // Store tokens after successful verification
      await this.storeTokens(response.tokens);
      
      // Store user data
      await AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(response.user));

      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  // Logout user
  async logout(): Promise<void> {
    try {
      // Clear all stored data
      await AsyncStorage.multiRemove([
        STORAGE_KEYS.AUTH_TOKEN,
        STORAGE_KEYS.REFRESH_TOKEN,
        STORAGE_KEYS.USER_DATA,
      ]);
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    try {
      const token = await AsyncStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
      return !!token;
    } catch (error) {
      return false;
    }
  }

  // Get current user data
  async getCurrentUser(): Promise<User | null> {
    try {
      const userData = await AsyncStorage.getItem(STORAGE_KEYS.USER_DATA);
      return userData ? JSON.parse(userData) : null;
    } catch (error) {
      return null;
    }
  }

  // Get stored auth token
  async getAuthToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
    } catch (error) {
      return null;
    }
  }

  // Refresh auth token
  async refreshToken(): Promise<AuthTokens> {
    try {
      const refreshToken = await AsyncStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await apiService.post<AuthTokens>(
        API_ENDPOINTS.REFRESH_TOKEN,
        { refresh: refreshToken }
      );

      await this.storeTokens(response);
      return response;
    } catch (error) {
      // If refresh fails, logout user
      await this.logout();
      throw this.handleAuthError(error);
    }
  }

  // Forgot password
  async forgotPassword(email: string): Promise<{ message: string }> {
    try {
      const response = await apiService.post<{ message: string }>(
        API_ENDPOINTS.FORGOT_PASSWORD,
        { email }
      );
      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  // Reset password
  async resetPassword(data: { 
    email: string; 
    otp: string; 
    new_password: string; 
  }): Promise<{ message: string }> {
    try {
      const response = await apiService.post<{ message: string }>(
        API_ENDPOINTS.RESET_PASSWORD,
        data
      );
      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  // Update profile
  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      const response = await apiService.put<User>(
        API_ENDPOINTS.UPDATE_PROFILE,
        userData
      );

      // Update stored user data
      await AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(response));
      
      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  // Private helper methods
  private async storeTokens(tokens: AuthTokens): Promise<void> {
    await AsyncStorage.multiSet([
      [STORAGE_KEYS.AUTH_TOKEN, tokens.access],
      [STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh],
    ]);
  }

  private handleAuthError(error: any): Error {
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.message || 
                     error.response.data?.detail || 
                     'Authentication failed';
      return new Error(message);
    } else if (error.request) {
      // Network error
      return new Error('Network error. Please check your connection.');
    } else {
      // Other error
      return new Error(error.message || 'An unexpected error occurred');
    }
  }
}

// Create and export singleton instance
export const authService = new AuthService();
export default authService;
