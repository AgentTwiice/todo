import React from 'react';
import { TouchableOpacity, Text, StyleSheet, useColorScheme } from 'react-native';
import { theme } from '../theme';

export interface ButtonProps {
  title: string;
  onPress: () => void;
}

export function Button({ title, onPress }: ButtonProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return (
    <TouchableOpacity onPress={onPress} style={[styles.button, { backgroundColor: colors.primary }]}>
      <Text style={[styles.text, { color: colors.surface }]}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    padding: 12,
    borderRadius: 4,
    alignItems: 'center',
  },
  text: {
    fontWeight: 'bold',
  },
});
