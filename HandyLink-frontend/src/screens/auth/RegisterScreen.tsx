import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Loading from '../../components/common/Loading';
import { authService } from '../../services/auth';

interface RegisterScreenProps {
  navigation?: any;
  onBack?: () => void;
}

const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation, onBack }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phoneNumber: '',
    password: '',
    confirmPassword: '',
    userType: 'customer',
  });

  type FormErrors = {
    firstName?: string;
    lastName?: string;
    email?: string;
    phoneNumber?: string;
    password?: string;
    confirmPassword?: string;
  };

  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: FormErrors = {};

    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.phoneNumber.trim()) {
      newErrors.phoneNumber = 'Phone number is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleRegister = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const registerData = {
        first_name: formData.firstName,
        last_name: formData.lastName,
        email: formData.email,
        phone_number: formData.phoneNumber,
        password: formData.password,
        password2: formData.confirmPassword,
        user_type: formData.userType,
      };

      await authService.register(registerData);

      Alert.alert(
        'Registration Successful',
        'Please check your email for verification instructions.',
        [
          {
            text: 'OK',
            onPress: () => {
              if (navigation) {
                navigation.navigate('Login');
              } else if (onBack) {
                onBack();
              }
            },
          },
        ]
      );
    } catch (error) {
      Alert.alert(
        'Registration Failed',
        'An error occurred during registration. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof FormErrors, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleUserTypeChange = (userType: string) => {
    setFormData(prev => ({ ...prev, userType }));
  };

  const handleBackPress = () => {
    if (onBack) {
      onBack();
    } else if (navigation) {
      navigation.goBack();
    }
  };

  if (loading) {
    return <Loading visible={true} message="Creating your account..." />;
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardAvoid}
      >
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.title}>🔧 Create Account</Text>
            <Text style={styles.subtitle}>Join HandyLink Today</Text>
          </View>

          {/* User Type Selection */}
          <View style={styles.userTypeContainer}>
            <Text style={styles.userTypeTitle}>I want to:</Text>
            <View style={styles.userTypeButtons}>
              <Button
                title="Find Services"
                variant={formData.userType === 'customer' ? 'primary' : 'outline'}
                onPress={() => handleUserTypeChange('customer')}
                style={styles.userTypeButtonLeft}
              />
              <Button
                title="Provide Services"
                variant={formData.userType === 'provider' ? 'primary' : 'outline'}
                onPress={() => handleUserTypeChange('provider')}
                style={styles.userTypeButtonRight}
              />
            </View>
          </View>

          {/* Form Fields */}
          <View style={styles.form}>
            <View style={styles.nameRow}>
              <Input
                label="First Name"
                value={formData.firstName}
                onChangeText={(value) => handleInputChange('firstName', value)}
                error={errors.firstName}
                placeholder="Enter your first name"
                style={styles.nameInputLeft}
              />
              <Input
                label="Last Name"
                value={formData.lastName}
                onChangeText={(value) => handleInputChange('lastName', value)}
                error={errors.lastName}
                placeholder="Enter your last name"
                style={styles.nameInputRight}
              />
            </View>

            <Input
              label="Email Address"
              value={formData.email}
              onChangeText={(value) => handleInputChange('email', value)}
              error={errors.email}
              placeholder="Enter your email address"
              keyboardType="email-address"
              autoCapitalize="none"
            />

            <Input
              label="Phone Number"
              value={formData.phoneNumber}
              onChangeText={(value) => handleInputChange('phoneNumber', value)}
              error={errors.phoneNumber}
              placeholder="Enter your phone number"
              keyboardType="phone-pad"
            />

            <Input
              label="Password"
              value={formData.password}
              onChangeText={(value) => handleInputChange('password', value)}
              error={errors.password}
              placeholder="Create a password"
              secureTextEntry
            />

            <Input
              label="Confirm Password"
              value={formData.confirmPassword}
              onChangeText={(value) => handleInputChange('confirmPassword', value)}
              error={errors.confirmPassword}
              placeholder="Confirm your password"
              secureTextEntry
            />
          </View>

          {/* Action Buttons */}
          <View style={styles.actions}>
            <Button
              title="Create Account"
              onPress={handleRegister}
              style={styles.registerButton}
            />
            
            <Button
              title="Back to Welcome"
              variant="outline"
              onPress={handleBackPress}
              style={styles.backButton}
            />
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              By creating an account, you agree to our Terms of Service and Privacy Policy
            </Text>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  keyboardAvoid: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: 20,
    paddingVertical: 30,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2563eb',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
  },
  userTypeContainer: {
    marginBottom: 30,
  },
  userTypeTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 12,
    textAlign: 'center',
  },
  userTypeButtons: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  userTypeButton: {
    flex: 1,
    maxWidth: 150,
  },
  userTypeButtonLeft: {
    flex: 1,
    maxWidth: 150,
    marginRight: 8,
  },
  userTypeButtonRight: {
    flex: 1,
    maxWidth: 150,
    marginLeft: 8,
  },
  form: {
    marginBottom: 30,
  },
  nameRow: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  nameInput: {
    flex: 1,
  },
  nameInputLeft: {
    flex: 1,
    marginRight: 8,
  },
  nameInputRight: {
    flex: 1,
    marginLeft: 8,
  },
  actions: {
    marginBottom: 20,
  },
  registerButton: {
    marginBottom: 12,
  },
  backButton: {
    marginBottom: 20,
  },
  footer: {
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 18,
  },
});

export default RegisterScreen;
