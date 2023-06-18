import * as React from 'react';
import RecentAccessScreen from "./src/screens/RecentAccess";
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import CreateUserScreen from "./src/screens/Create";
import { NavigationContainer } from '@react-navigation/native'
import { NativeBaseProvider } from "native-base";
import { GestureHandlerRootView } from 'react-native-gesture-handler';
const Stack = createNativeStackNavigator();
export default function App() {
  return (
      <NativeBaseProvider>
          <GestureHandlerRootView style={{ flex: 1 }}>
              <NavigationContainer>
                  <Stack.Navigator>
                      <Stack.Screen name="Access" component={RecentAccessScreen} options={{ headerShown: false}}/>
                      <Stack.Screen name="Create" component={CreateUserScreen} options={{ headerShown: false}}/>
                  </Stack.Navigator>
              </NavigationContainer>
          </GestureHandlerRootView>
      </NativeBaseProvider>
  );
}
