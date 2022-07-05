import tooltip from './Tooltip.js'

const tooltips_object = {
    initialize_synthpop : "Initialize synthetic population",
    run_simulation      : "Run simulation",
    change_location     : "Load a different municipality within this region",
    seed                : "Set seed. 0 for random seed.",
    infectious_count    : "Number of infectious agents at the start of the simulation.",
    cancel              : "Cancel running process.",
    status_init_synthpop : "Initializing synthetic population. This may take a few minutes.",
    status_run_cvabm    : "Running simulation. Please wait...",
    days                 : "Run until how many days"
}

export default{
    name: 'Parameters',
    props: {
        parametersProxy : Object,
        locationChoices : Object
    },
    components:{
        'Tooltip' : tooltip
    },
    setup(){

        const {ref} = Vue

        return{
            tooltips                        : tooltips_object,
            toggleChangeLocationDialogue    : ref(false),
            toggleLoading                   : ref(false),
            buttonHandler                   : ref(false),
            whichFunction                   : ref(''),
            
        }
    },
    template:
    `
    <q-form @submit = "$emit('run_function')">

        <div v-if = "!toggleLoading">
            <q-btn class = "parameter-button" round type = "submit" color="white" text-color="black" icon = "manage_accounts" @click = "buttonHandler = true">
                <Tooltip :content = tooltips.initialize_synthpop></Tooltip>
            </q-btn>
            <q-btn class = "parameter-button" round type = "submit" color="white" text-color="black" icon = "directions_run" @click = "buttonHandler = false">
                <Tooltip :content = tooltips.run_simulation></Tooltip>
            </q-btn>

        </div>

        <div v-else>
            <q-btn class = "parameter-button" round disabled type = "submit" color="white" text-color="black" icon = "manage_accounts">
                <Tooltip :content = tooltips.initialize_synthpop></Tooltip>
            </q-btn>
            <q-btn class = "parameter-button" round disabled type = "submit" color="white" text-color="black" icon = "directions_run">
                <Tooltip :content = tooltips.run_simulation></Tooltip>
            </q-btn>

            <span class = "parameter-button" style = "margin: 0">
                <!--<q-btn class = "parameter-button" round type = "submit" color="red" text-color="white" icon = "cancel">
                    <Tooltip :content = tooltips.cancel></Tooltip>
                </q-btn>-->

                <span v-if = "buttonHandler">
                    <q-spinner-grid
                        color="green"
                        size="2em"
                    />
                    <Tooltip :content = tooltips.status_init_synthpop></Tooltip>
                </span>
                <span v-else>
                    <q-spinner-gears
                        color="green"
                        size="2em"
                    />
                    <Tooltip :content = tooltips.status_run_cvabm></Tooltip>
                </span> 

            </span>
        </div>


        <br>

        <q-list bordered class="rounded-borders">
            <q-expansion-item
                expand-separator
                icon="perm_identity"
                label="Configurations"
                caption="Synthetic Population"
                default-opened
            >

                <q-card>
                    <q-card-section>
                        
                        <q-item style = "padding: 0">
                            <q-item-section>
                                <q-item-label>Region</q-item-label>
                            </q-item-section>
                            <q-item-section side>
                                <q-item-label caption>{{parametersProxy.location.region}}</q-item-label>
                            </q-item-section>
                        </q-item>

                        <q-item style = "padding: 0">
                            <q-item-section>
                                <q-item-label>Province</q-item-label>
                            </q-item-section>
                            <q-item-section side>
                                <q-item-label caption>{{parametersProxy.location.province}}</q-item-label>
                            </q-item-section>
                        </q-item>

                        <q-item style = "padding: 0">
                            <q-item-section>
                                <q-item-label>Municipality</q-item-label>
                            </q-item-section>
                            <q-item-section side>
                                <q-item-label caption>{{parametersProxy.location.municipality}}</q-item-label>
                            </q-item-section>
                        </q-item>

                        <br>

                        <q-btn round @click = "toggleChangeLocationDialogue = true" icon = "location_searching">
                            <Tooltip :content = tooltips.change_location></Tooltip>
                        </q-btn>

                        <q-dialog v-model = "toggleChangeLocationDialogue">
                            <q-card style = "min-width: 500px; padding: 10px" >

                                <q-card-section>
                                    <div class = "text-h6">Region</div>
                                    <span>{{parametersProxy.location.region}}</span>
                                </q-card-section>
                                

                                <q-card-section>
                                    <q-select 
                                        label = "Province"
                                        :options = locationChoices.provinces
                                        v-model = parametersProxy.location.province
                                    >
                                    <Tooltip></Tooltip>
                                    </q-select> 
                                </q-card-section>

                                <q-card-section>
                                    <q-select 
                                        label = "Municipality"
                                        :options = locationChoices.municipalities
                                        v-model = parametersProxy.location.municipality
                                    >
                                    </q-select> 
                                </q-card-section>

                                <q-btn label = "Confirm"></q-btn>
                                <q-btn label = "Cancel" @click = "toggleChangeLocationDialogue = false"></q-btn>
                            </q-card>
                        </q-dialog>

                        <br>
                        <br>

                        <q-input
                            id = "seed_input"
                            label="Seed"
                            label-slot
                            clearable
                            v-model = parametersProxy.seed
                        >
                        <Tooltip :content = tooltips.seed></Tooltip>
                        </q-input>

                    </q-card-section>

                </q-card>
                
            </q-expansion-item>

            <q-expansion-item
                expand-separator
                icon="coronavirus"
                label="Initial state"
                caption="Epidemiology"
                default-opened
            >
                <q-card>
                    <q-card-section>
                        <q-input
                        id = "infectious_count"
                        label="Infectious Count"
                        label-slot
                        clearable
                        v-model = parametersProxy.infectious_count
                        >
                            <Tooltip :content = tooltips.infectious_count></Tooltip>
                        </q-input>
                    </q-card-section>
                </q-card>

            </q-expansion-item>

            <q-expansion-item
                expand-separator
                icon="date_range"
                label="Timeline"
                caption="Temporal"
                default-opened
            >
                <q-card>
                    <q-card-section>
                        <q-input
                        id = "days"
                        label="Days"
                        label-slot
                        clearable
                        v-model = parametersProxy.days
                        >
                            <Tooltip :content = tooltips.days></Tooltip>
                        </q-input>
                    </q-card-section>
                </q-card>

            </q-expansion-item>


        </q-list>

    </q-form>
    `
}