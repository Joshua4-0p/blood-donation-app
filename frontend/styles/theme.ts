// frontend/styles/theme.ts
import { ImageSourcePropType } from 'react-native';

export const colors = {
  // Replace with Figma hex codes
  primary: '#000000', // Button color
  secondary: '#FFFFFF', // Text/background color
  background: '#000000', // Background color (if no image)
};

export const fonts = {
  // Replace with Figma font names and sizes
  regular: 'Roboto-Regular',
  bold: 'Roboto-Bold',
  size: {
    small: 14,
    medium: 16,
    large: 24,
  },
};

export const icons = {
  // Replace with Figma background image path
  background: require('../assets/images/onboarding-bg.png') as ImageSourcePropType,
};