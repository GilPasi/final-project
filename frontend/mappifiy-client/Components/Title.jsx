import React, { Component } from "react";
import { StyleSheet, View, Text } from "react-native";

function Index(props) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to {"\n"}Mappify!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 329,
    height: 150
  },
  title: {
    fontFamily: "AlNile-Bold",
    color: "rgba(98,114,84,1)",
    fontSize: 55,
    textAlign: "center"
  }
});

export default Index;
