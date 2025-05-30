import React from 'react';
import { Modal as RNModal, View, StyleSheet, useColorScheme } from 'react-native';
import { theme, spacing } from '../theme';

export interface ModalProps {
  visible: boolean;
  onRequestClose: () => void;
  children: React.ReactNode;
}

export function Modal({ visible, onRequestClose, children }: ModalProps) {
  const scheme = useColorScheme() || 'light';
  const colors = theme[scheme].colors;
  return (
    <RNModal visible={visible} transparent animationType="slide" onRequestClose={onRequestClose}>
      <View style={styles.backdrop}>
        <View style={[styles.container, { backgroundColor: colors.surface }]}>{children}</View>
      </View>
    </RNModal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',
    padding: spacing.md,
  },
  container: {
    borderRadius: 8,
    padding: spacing.md,
  },
});
