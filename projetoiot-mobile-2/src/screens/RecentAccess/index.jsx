import {useEffect, useState} from 'react';
import {FlatList, RefreshControl, Text, View} from 'react-native';
import { styles } from './styles'
import {Button, Image} from "native-base";
import {api} from "../../utils/api";

const months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul","Ago","Set","Out","Nov","Dez"];

const renderItem = (item) => {
    const date = new Date(item.created_at)
    date.setHours(date.getHours() - 3)
    const formatedDate = date.toLocaleString('pt-BR')

    return (
        <View style={styles.card}>
            <View style={{
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'center',
                justifyContent:'space-between',
                width: '100%'
            }}>
                <Image alt={item.id} source={{ uri: item.image }} style={{ width: 60, height: 60, borderRadius: 99}}/>
                <View
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'flex-end'
                    }}>
                    <Text style={styles.cardUserName}>{item.user_name}</Text>
                    <Text style={{
                        fontSize: 16,
                        color: item.allowed ? '#116A7B' : '#E97777'
                    }}>{item.allowed ? 'Permitido': 'Negado'}</Text>
                    <Text style={styles.cardDate}>{formatedDate}</Text>
                </View>
            </View>
        </View>
    )}
;


export default function RecentAccessScreen({ navigation }) {
    const [logs, setLogs] = useState([])
    const [refreshing, setRefreshing] = useState(true);

    useEffect(() => {
        setRefreshing(true)
        api.get('logs')
            .then(({data}) => {
                setLogs(data)
                setRefreshing(false)
            })
    }, [])


    return (
        <View style={styles.content}>
            <View style={styles.container}>
                <Text style={styles.title}>Acessos recentes</Text>
                {refreshing && <Text>Carregando...</Text>}
                 <FlatList
                    data={logs}
                    refreshControl={
                        <RefreshControl
                            refreshing={refreshing}
                            onRefresh={() => {
                                setRefreshing(true)
                                api.get('logs')
                                    .then(({data}) => {
                                        setLogs(data)
                                        setRefreshing(false)
                                    })
                            }}
                        />
                    }
                    style={{ flex: 1 }}
                    renderItem={({item}) => renderItem(item)}
                    keyExtractor={item => item.id}
                />
                <Button onPress={() => navigation.navigate('Create')} padding="3" style={{backgroundColor: '#0C0F14', marginTop: 24}} >
                    <Text style={{color: '#FFF', fontWeight: 'bold'}}>Criar usuário</Text>
                </Button>
            </View>
        </View>
    )
}
