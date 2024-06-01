import React, { useEffect } from 'react';
import { StyleSheet, View, Text } from 'react-native';
import useLoadFonts from '../Hooks/useLoadFonts'; // Adjust the path accordingly

export default function Title({ text, size }) {
  const styles = StyleSheet.create({
    container: {},
    title: {
      fontFamily: 'Alef-Bold',
      color: 'rgba(98,114,84,1)',
      fontSize: size ? size : 55,
      textAlign: 'center',
    },
  });

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{text}</Text>
    </View>
  );
}
