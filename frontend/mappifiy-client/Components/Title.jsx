import React, { Component } from "react";
import { StyleSheet, View, Text } from "react-native";

export default function Title({text, size}) {

const styles = StyleSheet.create({
    container: {},
    title: {
      fontFamily: "AlNile-Bold",
      color: "rgba(98,114,84,1)",
      fontSize: size ? size : 55,
      textAlign: "center"
    }
  });

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{text}</Text>
    </View>
  );
}

