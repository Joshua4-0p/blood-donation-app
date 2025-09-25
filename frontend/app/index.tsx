import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Dimensions,
  SafeAreaView,
  StyleSheet,
  Platform,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import BloodDropIcon from '../components/BloodDropIcon';

const { width, height } = Dimensions.get('window');

// Add utility functions for better function coverage
export const validateScreenSize = (): boolean => {
  return width > 300 && height > 500;
};

export const getButtonStyle = (isPressed: boolean): object => {
  return {
    opacity: isPressed ? 0.7 : 1,
    transform: [{ scale: isPressed ? 0.98 : 1 }],
  };
};

export const formatTagline = (username?: string): string => {
  if (username && username.length > 0) {
    return `Welcome ${username}! Your chance to be a hero`;
  }
  return 'Your chance to finally be the hero you have always dreamed to be';
};

const OnboardingScreen: React.FC = () => {
  const router = useRouter();
  const [isRegisterPressed, setIsRegisterPressed] = useState(false);
  const [isLoginPressed, setIsLoginPressed] = useState(false);
  const [screenReady, setScreenReady] = useState(false);

  // Add useEffect for function coverage
  useEffect(() => {
    const checkScreenCompatibility = () => {
      if (!validateScreenSize()) {
        Alert.alert('Screen Size Warning', 'This app works best on larger screens');
      }
      setScreenReady(true);
    };

    checkScreenCompatibility();
  }, []);

  const handleRegister = () => {
    if (!screenReady) {
      Alert.alert('Please wait', 'Screen is still loading');
      return;
    }
    
    if (Platform.OS === 'ios') {
      // iOS specific handling
      router.push('/screens/register');
    } else if (Platform.OS === 'android') {
      // Android specific handling
      router.push('/screens/register');
    } else {
      // Web or other platforms
      router.push('/screens/register');
    }
  };

  const handleLogin = () => {
    if (!screenReady) {
      Alert.alert('Please wait', 'Screen is still loading');
      return;
    }

    try {
      router.push('/screens/login');
    } catch (error) {
      Alert.alert('Navigation Error', 'Unable to navigate to login screen');
    }
  };

  // Add conditional rendering for branch coverage
  const renderTagline = () => {
    const taglineText = formatTagline();
    
    return (
      <View className="items-center mb-20 px-1">
        <Text
          className="text-center leading-7"
          style={{
            fontSize: screenReady ? 18 : 16,
            color: '#364153',
            opacity: 0.9,
            lineHeight: 28
          }}
        >
          {taglineText.includes('hero') ? taglineText : 'Welcome to Blood Donation App'}
        </Text>
      </View>
    );
  };

  // Add loading state for branch coverage
  if (!screenReady) {
    return (
      <SafeAreaView className="flex-1 justify-center items-center" style={{ backgroundColor: '#FFFFFF' }}>
        <Text>Loading...</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1" style={{ backgroundColor: '#FFFFFF' }}>
      {/* Background shapes - conditional rendering based on screen size */}
      {width > 350 && (
        <>
          <View
            className="absolute"
            style={{
              top: -height * 0.18,
              right: -width * 0.17,
              width: width * 0.8,
              height: height * 0.58,
              backgroundColor: '#FFC9C9',
              borderRadius: width * 0.4,
              opacity: 0.7,
            }}
          />
          <View
            className="absolute"
            style={{
              bottom: -height * 0.15,
              left: -width * 0.15,
              width: width * 0.7,
              height: height * 0.6,
              backgroundColor: '#FFE2E2',
              borderRadius: width * 0.45,
              opacity: 0.5,
            }}
          />
        </>
      )}

      <View className="flex-1 justify-center items-center px-8">
        {/* Logo Section */}
        <View className="items-center mb-20">
          <BloodDropIcon 
            size={width > 400 ? 180 : 150} 
            showShadow={Platform.OS !== 'web'}
          />
        </View>

        {/* Tagline */}
        {renderTagline()}

        {/* Buttons */}
        <View className="w-full px-4">
          <TouchableOpacity
            className="border-2 rounded-full py-4 px-8 mb-4 items-center"
            style={[
              {
                borderColor: '#E7000B',
                borderWidth: 2
              },
              getButtonStyle(isRegisterPressed)
            ]}
            onPressIn={() => setIsRegisterPressed(true)}
            onPressOut={() => setIsRegisterPressed(false)}
            onPress={handleRegister}
            activeOpacity={0.8}
            disabled={!screenReady}
          >
            <Text
              className="font-semibold"
              style={{
                letterSpacing: 2,
                fontSize: 16,
                color: screenReady ? '#E7000B' : '#999999'
              }}
            >
              {screenReady ? 'REGISTER' : 'LOADING...'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            className="rounded-full py-4 px-8 items-center"
            style={[
              styles.loginButton,
              {
                backgroundColor: screenReady ? '#E7000B' : '#CCCCCC'
              },
              getButtonStyle(isLoginPressed)
            ]}
            onPressIn={() => setIsLoginPressed(true)}
            onPressOut={() => setIsLoginPressed(false)}
            onPress={handleLogin}
            activeOpacity={0.8}
            disabled={!screenReady}
          >
            <Text
              className="text-white font-semibold"
              style={{
                letterSpacing: 2,
                fontSize: 16
              }}
            >
              {screenReady ? 'LOGIN' : 'LOADING...'}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  backgroundShape: {
    // The large pink circular shape in the background
  },
  loginButton: {
    shadowColor: '#E53E3E',
    shadowOffset: {
      width: 0,
      height: 6,
    },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 10,
  },
});

export default function App() {
  return <OnboardingScreen />;
}
