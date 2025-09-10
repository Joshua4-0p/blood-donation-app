# Welcome to your Expo app 👋

This is an [Expo](https://expo.dev) project created with [`create-expo-app`](https://www.npmjs.com/package/create-expo-app).

## Get started

1. Install dependencies

   ```bash
   npm install
   ```

2. Start the app

   ```bash
   npx expo start
   ```

In the output, you'll find options to open the app in a

- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), a limited sandbox for trying out app development with Expo

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

## Get a fresh project

When you're ready, run:

```bash
npm run reset-project
```

This command will move the starter code to the **app-example** directory and create a blank **app** directory where you can start developing.

## Learn more

To learn more about developing your project with Expo, look at the following resources:

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.








DON8 Blood Donation App (React Native + Tailwind v3 + NativeWind v4)
  Frontend setup for blood donation app based on Figma design.
Prerequisites

Node.js LTS 20+
Expo CLI latest
Expo Go app

Setup

Create project: npx create-expo-app@latest don8Blood --template blank
Install: npm i nativewind@latest tailwindcss@^3.4.17 react-native-reanimated@latest react-native-safe-area-context@latest expo@latest react-native-worklets@latest
Create tailwind.config.js manually with content paths and NativeWind preset.
Create styles/global.css with Tailwind directives.
Update babel.config.js with react-native-worklets/plugin.
Update metro.config.js with NativeWind integration.
Add types/nativewind-env.d.ts for TS.
Run: npx expo start --clear

Usage Notes

Use className for Tailwind v3 classes.
Add Figma assets to assets/.
Extend tailwind.config.js with Figma colors.
Use boxShadow instead of shadow*, style.pointerEvents instead of props.pointerEvents, props.resizeMode instead of style.resizeMode.
Directory: See directory-structure.md.

Troubleshooting

react-native-worklets/plugin missing? Install with npm i react-native-worklets@latest.
Deprecated props? Replace with modern equivalents (see Usage Notes); check Expo Router if warnings persist.
Bundling fails? Clear cache with --clear.
Missing modules? Reinstall with npm install.
# Directory Structure for DON8Blood App
- `app/`: Expo Router screens/routes (e.g., onboarding in `index.tsx`, tabs for list/map/profile).
- `components/`: Reusable Figma-inspired UI (e.g., red buttons, form inputs).
- `assets/`: Figma exports (e.g., blood drop PNGs in `images/`).
- `styles/`: Tailwind v4 CSS config.
- `nativewind-env.d.ts`: NativeWind TypeScript support.
- `babel.config.js`: Babel config with react-native-worklets/plugin.
- `metro.config.js`: Metro bundler config with NativeWind.
- `tailwind.config.js`: Tailwind v4 config with NativeWind preset and Figma colors.
- `package.json`: Project dependencies and scripts.