export default{
    name: 'Tooltip',
    props: {
        content: String,
        show: Boolean
    },
    setup(){
        const {ref} = Vue
        const show = ref(false)

        return{
            show
        }
    },
    template:
    `
        <q-tooltip class = "bg-blue-grey-8 parameter-tooltip" v-model = "show" anchor="center right" self="center left" :offset=[10,0]>
            {{content}}
        </q-tooltip>
    `

}