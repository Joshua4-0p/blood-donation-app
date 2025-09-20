module.exports = {
   preset: "react-native",
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest",
  },
  setupFiles: ["<rootDir>/jest.setup.js"], // <-- add this
  setupFilesAfterEnv: ["@testing-library/jest-native/extend-expect"],
  testPathIgnorePatterns: ["/node_modules/", "/android/", "/ios/"],
  moduleNameMapper: {
    "^expo-router$": "<rootDir>/__mocks__/expo-router.js",
    "^expo$": "<rootDir>/__mocks__/expo.js",
  },
  transformIgnorePatterns: [
    "node_modules/(?!(react-native|@react-native|expo-modules-core|react-clone-referenced-element|expo-router)/)"
  ],
  moduleFileExtensions: [
    "ts",
    "tsx",
    "js",
    "jsx",
    "json",
    "node",
    "ios.js",
    "android.js"
  ]
};
