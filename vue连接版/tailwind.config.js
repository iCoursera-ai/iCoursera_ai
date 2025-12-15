module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#165DFF',
        secondary: '#6B7280',
        light: '#F9FAFB',
        dark: '#1F2937',
        success: '#10B981',
        gray: {
          100: '#F7F8FA',
          200: '#E5E6EB',
          300: '#C9CDD4',
          400: '#86909C',
          500: '#4E5969',
          600: '#272E3B',
        },
        red: {
          500: '#F53F3F',
        },
        orange: {
          500: '#FF7D00',
        }
      },
      fontFamily: {
        inter: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}