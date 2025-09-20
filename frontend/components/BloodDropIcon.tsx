import React from 'react';
import { Image, View } from 'react-native';

interface BloodDropIconProps {
  size?: number;
}

const BloodDropIcon: React.FC<BloodDropIconProps> = ({ size = 80 }) => {
  return (
    <View className="justify-center items-center">
      <Image 
        source={require('../assets/images/blood-drop.png')} // You'll need to save your blood drop image here
        style={{ 
          width: size, 
          height: size,
          resizeMode: 'contain' 
        }}
      />
    </View>
  );
};

export default BloodDropIcon;