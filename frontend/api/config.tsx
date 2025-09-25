// api/config.ts
export const API_BASE_URL = 'http://localhost:3000/api'; // Replace with backend URL
export const API_HEADERS: Record<string, string> = {
  'Content-Type': 'application/json',
  // Add auth token if needed: 'Authorization': `Bearer ${token}`
};

import AsyncStorage from '@react-native-async-storage/async-storage';

// Save token (token is always a string)
export const setToken = async (token: string): Promise<void> => {
  await AsyncStorage.setItem('token', token);
};

// Get token (may return null if not set)
export const getToken = async (): Promise<string | null> => {
  return await AsyncStorage.getItem('token');
};
