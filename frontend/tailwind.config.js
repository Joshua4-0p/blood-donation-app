/** @type {import('tailwindcss').Config} */
  module.exports = {
    content: [
      "./app/**/*.{js,jsx,ts,tsx}",
      "./components/**/*.{js,jsx,ts,tsx}",
      "./screens/**/*.{js,jsx,ts,tsx}",
    ],
    presets: [require("nativewind/preset")],
    theme: {
        extend: {
          colors: {
            'don8-primary': '#E53E3E',
            'don8-text': '#1A365D',
            'don8-bg': '#FDF2F8',
            'don8-shape': '#F8BBD9',
          }
        },
      },
    plugins: [],
  };