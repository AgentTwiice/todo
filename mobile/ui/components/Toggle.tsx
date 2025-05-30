import React from 'react';
import { Switch, useColorScheme } from 'react-native';
import { theme } from '../theme';

export interface ToggleProps {
  value: boolean;
  onValueChange: (val: boolean) => void;
}

export function Toggle({ value, onValueChange }: ToggleProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return <Switch value={value} onValueChange={onValueChange} trackColor={{ true: colors.primary }} />;
}
