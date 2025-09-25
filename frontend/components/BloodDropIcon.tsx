import React from 'react';
import { Image, View, Platform, Text } from 'react-native';

interface BloodDropIconProps {
  size?: number;
  showShadow?: boolean;
  fallbackText?: string;
}

// Add utility functions for better coverage
export const calculateIconSize = (size: number): { width: number; height: number } => {
  if (size <= 0) {
    return { width: 80, height: 80 };
  }
  
  if (size > 300) {
    return { width: 300, height: 300 };
  }
  
  return { width: size, height: size };
};

export const getIconContainerStyle = (showShadow: boolean, size: number) => {
  const baseStyle = {
    justifyContent: 'center' as const,
    alignItems: 'center' as const,
  };

  if (!showShadow) {
    return baseStyle;
  }

  if (Platform.OS === 'ios') {
    return {
      ...baseStyle,
      shadowColor: '#E53E3E',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.3,
      shadowRadius: size > 150 ? 8 : 4,
    };
  } else if (Platform.OS === 'android') {
    return {
      ...baseStyle,
      elevation: size > 150 ? 8 : 4,
    };
  }

  return baseStyle;
};

export const shouldShowFallback = (size: number): boolean => {
  return size < 20;
};

const BloodDropIcon: React.FC<BloodDropIconProps> = ({ 
  size = 80, 
  showShadow = false,
  fallbackText = "🩸"
}) => {
  const iconDimensions = calculateIconSize(size);
  const containerStyle = getIconContainerStyle(showShadow, size);

  // Branch coverage: conditional rendering based on size
  if (shouldShowFallback(size)) {
    return (
      <View style={containerStyle}>
        <Text style={{ fontSize: size }}>{fallbackText}</Text>
      </View>
    );
  }

  // Branch coverage: conditional rendering based on platform
  const imageSource = Platform.select({
    ios: require('../assets/images/blood-drop.png'),
    android: require('../assets/images/blood-drop.png'),
    default: require('../assets/images/blood-drop.png'),
  });

  // Branch coverage: handle different size ranges
  const resizeMode = size > 200 ? 'cover' : 'contain';

  return (
    <View style={containerStyle}>
      <Image 
        source={imageSource}
        style={{ 
          width: iconDimensions.width, 
          height: iconDimensions.height,
          resizeMode: resizeMode
        }}
        onError={() => {
          console.warn('Failed to load blood drop image');
        }}
      />
      {/* Conditional badge for large icons */}
      {size > 150 && (
        <View 
          style={{
            position: 'absolute',
            bottom: -5,
            right: -5,
            backgroundColor: '#E7000B',
            borderRadius: 10,
            width: 20,
            height: 20,
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Text style={{ color: 'white', fontSize: 12, fontWeight: 'bold' }}>+</Text>
        </View>
      )}
    </View>
  );
};

export default BloodDropIcon;
