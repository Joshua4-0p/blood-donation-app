import { View, Text } from "react-native";
  import "../styles/global.css";

  export default function App() {
    return (
      <View className="flex-1 items-center justify-center bg-pink-100" style={{ boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
        <Text className="text-red-500 font-bold text-xl" style={{ pointerEvents: "auto" }}>Welcome to Don8!</Text>
        <Text className="text-center">Your Chance to finally be the hero you have always dreamt to be</Text>
      </View>
    );
  }