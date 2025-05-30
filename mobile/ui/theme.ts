export const colors = {
  primary: '#6200ee',
  background: '#ffffff',
  surface: '#ffffff',
  text: '#000000',
  muted: '#6b6b6b',
  lightBackground: '#f2f2f2',
  darkBackground: '#121212',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const typography = {
  h1: 32,
  h2: 24,
  body: 16,
  caption: 12,
};

export const theme = {
  light: {
    colors: {
      background: colors.background,
      text: colors.text,
      surface: colors.surface,
      primary: colors.primary,
    },
  },
  dark: {
    colors: {
      background: colors.darkBackground,
      text: colors.surface,
      surface: '#1e1e1e',
      primary: colors.primary,
    },
  },
};

export type ThemeMode = keyof typeof theme;
