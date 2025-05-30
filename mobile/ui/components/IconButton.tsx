import React from 'react';
import { TouchableOpacity, Text, StyleSheet, useColorScheme } from 'react-native';
import { theme } from '../theme';

export interface IconButtonProps {
  icon: string;
  onPress: () => void;
}

export function IconButton({ icon, onPress }: IconButtonProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return (
    <TouchableOpacity onPress={onPress} style={[styles.button, { backgroundColor: colors.primary }]}>
      <Text style={{ color: colors.surface }}>{icon}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    padding: 8,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
