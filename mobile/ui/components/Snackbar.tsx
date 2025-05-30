import React from 'react';
import { View, Text, StyleSheet, useColorScheme } from 'react-native';
import { theme, spacing } from '../theme';

export interface SnackbarProps {
  message: string;
}

export function Snackbar({ message }: SnackbarProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return (
    <View style={[styles.container, { backgroundColor: colors.primary }]}>
      <Text style={{ color: colors.surface }}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    bottom: spacing.lg,
    left: spacing.md,
    right: spacing.md,
    padding: spacing.sm,
    borderRadius: 4,
    alignItems: 'center',
  },
});
