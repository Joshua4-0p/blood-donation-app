import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Dimensions,
  SafeAreaView,
  StyleSheet,
} from 'react-native';
import { useRouter } from 'expo-router';
import BloodDropIcon from '../components/BloodDropIcon';

const { width, height } = Dimensions.get('window');

const OnboardingScreen: React.FC = () => {
  const router = useRouter();

  const handleRegister = () => {
    router.push('/screens/register');
  };

  const handleLogin = () => {
    router.push('/screens/login');
  };

  return (
      <SafeAreaView className="flex-1" style={{ backgroundColor: '#FFFFFF' }}>
        {/* Top Right Oval Shape */}
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

        {/* Bottom Left Oval Shape */}
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

        <View className="flex-1 justify-center items-center px-8">
          {/* Logo Section */}
          <View className="items-center mb-20">
            <BloodDropIcon size={180} />
          </View>

          {/* Tagline */}
          <View className="items-center mb-20 px-1">
            <Text
              className="text-center leading-7"
              style={{
                fontSize: 18,
                color: '#364153',
                opacity: 0.9,
                lineHeight: 28
              }}
            >
              Your chance to finally be the hero {'\n'} you have always dreamed to be
            </Text>
          </View>

          {/* Buttons */}
          <View className="w-full px-4">
            <TouchableOpacity
              className="border-2 rounded-full py-4 px-8 mb-4 items-center"
              style={{
                borderColor: '#E7000B',
                borderWidth: 2
              }}
              onPress={handleRegister}
              activeOpacity={0.8}
            >
              <Text
                className="font-semibold"
                style={{
                  letterSpacing: 2,
                  fontSize: 16,
                  color: '#E7000B'
                }}
              >
                REGISTER
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              className="rounded-full py-4 px-8 items-center"
              style={[
                styles.loginButton,
                {
                  backgroundColor: '#E7000B'
                }
              ]}
              onPress={handleLogin}
              activeOpacity={0.8}
            >
              <Text
                className="text-white font-semibold"
                style={{
                  letterSpacing: 2,
                  fontSize: 16
                }}
              >
                LOGIN
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