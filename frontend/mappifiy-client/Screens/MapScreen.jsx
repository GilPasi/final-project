
import { Image } from 'expo-image';
import { StyleSheet, View, TextInput, Text } from 'react-native';
import {getBaseUrl} from '../utilities/utils'
import {useState, useEffect} from 'react'
import ThemedButton from '../Components/ThemedButton';
import Option from '../Components/Option'
import {api} from '../services/api'

const undressFullPath = path => path.split("/").pop().split(".")[0]

export default function App() {
  const [mapName, setMapName] = useState('')
  const [allMaps, setAllMaps] = useState([])

  useEffect(()=>{
    api.get('media/maps/all/')
    .then(response => {
      console.log(response.data.files)
      setAllMaps(response.data.files)

    })
    .catch(err => console.log(`ERROR: A problem has 
    occured while trying to fetch all images names ${err}`))
  },[])

  
  return (
    <View style={styles.container}>
      {/* <View style={styles.searchBar}>
        <TextInput
          style={styles.input}
          placeholder="Type location..."
          value={mapName}
          onChangeText={mapName => setMapName(mapName)}
        /> 
        <ThemedButton title="Find" size="small"/>
      </View> */}
      {allMaps.map(
        location =>{
          location = undressFullPath(location)
          return(<Option 
                  key={location}
                  text={`${location}${'\t'}${'\t'}${'\t'} 	➯`}
                  value={location}
                  onPress={mapName => {
                    console.log(`${getBaseUrl()}/api/media/maps/${mapName}.png`)
                    setMapName(mapName)}}
            />)
        })}

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
    width:"100%",
    alignItems: 'center',
  },
});
