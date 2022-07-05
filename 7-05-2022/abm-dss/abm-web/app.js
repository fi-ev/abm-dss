import header from './components/Header.js'
import footer from './components/Footer.js'
import body from './components/Body.js'

const app = Vue.createApp({
    components:{
        'Header': header,
        'Body'  : body,
        'Footer': footer
    },  
    setup(){
        const $q = Quasar.useQuasar()
        const {axios} = 'axios'
        
        return
            {

        }
    },
    template:
    `
    <q-layout view="lHh lpr lFf">
        <Header></Header>
        <Body></Body>
        <Footer></Footer>
    </q-layout>
    `

})

app.use(Quasar)
app.mount('#app')