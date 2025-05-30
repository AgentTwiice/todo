import React from 'react';
import { View, Text, StyleSheet, useColorScheme } from 'react-native';
import { theme } from '../theme';

export interface AvatarProps {
  label: string;
}

export function Avatar({ label }: AvatarProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return (
    <View style={[styles.container, { backgroundColor: colors.primary }]}>
      <Text style={{ color: colors.surface }}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
