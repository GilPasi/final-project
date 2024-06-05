
import { Image } from 'expo-image';
import { StyleSheet, View,TextInput } from 'react-native';
import {getBaseUrl} from '../utilities/utils'
import {useState} from 'react'
import ThemedButton from '../Components/ThemedButton';

export default function App() {
  const [mapName, setMapName] = useState('')
  

  

  

  return (
    <View style={styles.container}>
      <View style={styles.searchBar}>
        <TextInput
          style={styles.input}
          placeholder="Type here..."
          value={mapName}
          onChangeText={text => setMapName(text)}
        /> 
        <ThemedButton title="Find" size="small"/>
      </View>

    <Image 
        source= {`${getBaseUrl()}/api/media/maps/${mapName}.png`}
        style={styles.image}
       />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    flex: 1,
    width: '100%',
    backgroundColor: '#0553',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    paddingHorizontal: 10,
    width: '80%',
    marginBottom: 20,
  },
  searchBar:{
    // backgroundColor:"red",
    width:"100%",
    alignItems: 'center',
  },
});
