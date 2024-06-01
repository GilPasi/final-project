import { StyleSheet, View, Text } from 'react-native';
import theme from './StaticStyle';

export default function Title({ text, size }) {

  const styles = StyleSheet.create({
    container: {},
    title: {
      fontFamily: theme.fonts.primary,
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
