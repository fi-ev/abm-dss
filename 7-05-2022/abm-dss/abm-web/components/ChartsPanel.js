
import barchartd3 from '../charts/dthree/BarChart.js'

export default{
    name: 'Charts',
    components: {
        'BarChartd3' : barchartd3,
    },
    setup(){

        const {onMounted} = Vue;

        function CreateCharts(){
            
            //console.log('Create Charts')
            //barangay charts
            axios.get('http://127.0.0.1:5000/abmbe/get/synthpop/barangays')
            .then((response) => {

                console.log(response.data)

            })

            //population chart
        }

        
        return {
            CreateCharts
        }
    },
    template:
    `
    `
}