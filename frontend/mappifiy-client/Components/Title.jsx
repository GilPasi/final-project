import { StyleSheet, View, Text } from 'react-native';
import theme from './StaticStyle';

export default function Title({ text, size, isError }) {
  size = (typeof size === 'string' || size instanceof String) ? theme.fontSizes[size] : size
  const styles = StyleSheet.create({
    container: {},
    title: {
      fontFamily: theme.fonts.primary,
      color: isError ? theme.colors.error : theme.colors.primary,
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
