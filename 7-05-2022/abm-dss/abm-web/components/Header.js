export default{
    name: 'Header',
    setup(){

    },
    template:
    `
        <q-header class = "header text-dark" bordered>
            <q-toolbar>
                <q-avatar>
                    <img src="static/nicer-logo-1.png">
                </q-avatar>
                <q-toolbar-title class = "text-center">
                    COVID-19 Transmission Model for Mindanao   
                </q-toolbar-title>
            </q-toolbar>
        </q-header>

    `
}