import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import theme from "./StaticStyle";

const LoadingBar = ({ progress }) => {
  return (
    <View style={styles.container}>
      <View style={styles.progressBar}>
        <View style={[styles.progress, { width: `${progress}%` }]} />
      </View>
      <Text style={styles.progressText}>{progress}%</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 20,
  },
  progressBar: {
    width: "100%",
    height: 50,
    backgroundColor: '#e0e0df',
    borderRadius: 10,
    overflow: 'hidden',
    borderWidth: 5,
    borderColor: theme.colors.secondary, 
  },
  progress: {
    height: '100%',
    backgroundColor: theme.colors.primary,
  },
  progressText: {
    marginTop: 10,
    fontSize: 16,
    color: '#000',
  },
});

export default LoadingBar;
