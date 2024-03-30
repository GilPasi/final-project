import React, { Component } from "react";
import { StyleSheet, View, Text } from "react-native";
import theme from "./StaticStyle"

function Button(props) {
  return (
    <View style={styles.container}>
        <Text>{props.text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 280,
    height: 88, 
    backgroundColor: theme.colors.secondary,
  },
});

export default Button;
