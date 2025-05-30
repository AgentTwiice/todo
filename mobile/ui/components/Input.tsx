import React from 'react';
import { TextInput, StyleSheet, useColorScheme } from 'react-native';
import { theme, spacing } from '../theme';

export interface InputProps {
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  secureTextEntry?: boolean;
}

export function Input({ value, onChangeText, placeholder, secureTextEntry }: InputProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return (
    <TextInput
      style={[styles.input, { backgroundColor: colors.surface, color: colors.text }]}
      placeholder={placeholder}
      placeholderTextColor={colors.muted}
      value={value}
      secureTextEntry={secureTextEntry}
      onChangeText={onChangeText}
    />
  );
}

const styles = StyleSheet.create({
  input: {
    padding: spacing.sm,
    borderRadius: 4,
    marginBottom: spacing.sm,
    borderWidth: 1,
    borderColor: '#ccc',
  },
});
