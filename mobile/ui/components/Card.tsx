import React from 'react';
import { View, StyleSheet, useColorScheme } from 'react-native';
import { theme, spacing } from '../theme';

export interface CardProps {
  children: React.ReactNode;
  style?: object;
}

export function Card({ children, style }: CardProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return <View style={[styles.card, { backgroundColor: colors.surface }, style]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    padding: spacing.md,
    borderRadius: 8,
    marginBottom: spacing.sm,
    elevation: 2,
  },
});
