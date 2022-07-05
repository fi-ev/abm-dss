import parameters from './ParametersPanel.js'
import chartspanel from './ChartsPanel.js'

const parameter_object = {
    location : {
        region: '',
        province: '',
        municipality: '',
    },

    seed: 0,

    infectious_count: 1,
    
    days: 1,
}

const location_choices = {
    provinces:      [],
    municipalities: []
}

export default{
    name: 'Body',
    components: {
        'Parameters'  : parameters,
        'ChartsPanel': chartspanel
    },
    setup(){
        const {ref, onMounted, reactive}    = Vue
        const parameter_proxy               = reactive(parameter_object)
        const locations                     = location_choices

        const chartjspanel = ref(null)
        const parameters   = ref(null)

        const $q                            = Quasar.useQuasar()
        //temporary region. change to actual user region.
        const region = 'Soccsksargen'


        onMounted(() => {
            //get the region data
            axios.get('http://127.0.0.1:5000/abmbe/get/'+ region)
            .then((response) => {

                const defaults = response.data['defaults']
                
                //set the parameter object
                //set defaults first
                parameter_proxy.location.region         = region
                parameter_proxy.location.province       = defaults['provinces']
                parameter_proxy.location.municipality   = defaults['municipality']
                
                //set user choices for location
                locations.provinces = Object.keys(response.data['provinces'])
                locations.municipalities = Object.values(response.data['provinces'][parameter_proxy.location.province])     

            })
            .catch((error) => {
                console.log(`cannot fetch data ${error.response}`)
            })
        })

        function RunWhichFunction(){
            if(parameters.value.buttonHandler == true)
            {
                InitializeSynthPop()
            }
            else{
                RunCovidAbm()
            }
        }

        //Initialize Synthpop
        function InitializeSynthPop(){

            parameters.value.toggleLoading = !parameters.value.toggleLoading
            
            //show loading screen
            //$q.loading.show({
            //    message: 'Initializing synthetic population. This may take a few minutes...',//'Initializing synthetic population. This may take a few minutes...'
            //    html: true
            //})
            //make an api call to synthpop and pass the parameter object as data
            axios.post('http://127.0.0.1:5000/abmbe/post/initialize_synthpop',
            {
                parameter_proxy
               
            })
            .then((response) => {
                
                parameters.value.toggleLoading = !parameters.value.toggleLoading
                
                console.log(response.data)

                //make sure response is successful
                if (response.data === 'success'){
                   
            
                    //and create charts by calling charts child component
                    chartjspanel.value.CreateCharts()
                    
                    //then hide loading screen
                    // $q.loading.hide()

                    //then notify user
                    $q.notify({
                        position: 'bottom',
                        message:'Successfully initialized population!',
                        color: 'positive',
                    })

                }
                else{
                    
                    //hide loading screen
                    //$q.loading.hide()

                    $q.notify({
                        position: 'bottom',
                        message:'Oh no. Something went wrong.',
                        color: 'red',
                    })
                }

            })
            

            
        }
        
        function RunCovidAbm(){

            parameters.value.toggleLoading = !parameters.value.toggleLoading

            axios.post('http://127.0.0.1:5000/abmbe/post/run_covid_abm',{
                parameter_proxy
            })
            .then((response)=>{
                console.log(response.data)
                parameters.value.toggleLoading = !parameters.value.toggleLoading
                
                if(response.data === 'success'){

                    $q.notify({
                        position: 'bottom',
                        message:'Successfully ran simulation!',
                        color: 'positive',
                    })
                }
                else{
                    
                    //hide loading screen
                    //$q.loading.hide()

                    $q.notify({
                        position: 'bottom',
                        message:'Oh no. Something went wrong.',
                        color: 'red',
                    })
                }
            })
        }

        return{
            splitterModel : ref(30),
            tab           : ref('synthpop'),
            chartjspanel,
            parameters,
            parameter_proxy,
            locations,

            RunWhichFunction,
            InitializeSynthPop,
            RunCovidAbm,
        }
    },

    template:
    `
    <q-page-container>
        <q-splitter v-model="splitterModel" style="height: 42rem">

        <template v-slot:before>
                
            <div class = "left-panel">
                <br>
                    <!--<Parameters ref = "parameters" :parametersProxy = parameter_proxy  :locationChoices = locations @initialize_synthpop = "InitializeSynthPop()"></Parameters>-->
                    <Parameters ref = "parameters" :parametersProxy = parameter_proxy  :locationChoices = locations @run_function = "RunWhichFunction()"></Parameters>
                <br>
            </div>

        </template>

        <template v-slot:after>

            <q-card>
                <q-tabs
                    v-model="tab"
                    dense
                    class="text-grey"
                    active-color="primary"
                    indicator-color="primary"
                    align="justify"
                    narrow-indicator
                >
                    <q-tab name="synthpop" label="Synthetic Population" />
                    <q-tab name="covid" label="COVID-19 Analysis" />
                </q-tabs>

                <q-separator />

                <q-tab-panels v-model="tab" animated>
                    <q-tab-panel name="synthpop">
                        <ChartsPanel ref = "chartjspanel"></ChartsPanel>
                    </q-tab-panel>

                    <q-tab-panel name="covid">
                    </q-tab-panel>
                </q-tab-panels>

            </q-card>
        </template>

        </q-splitter>
    </q-page-container>
    `
}