municipality_aliases = {
    'general_santos' : ['General Santos', 
                        'GENERAL SANTOS', 
                        'General Santos City', 
                        'GENERAL SANTOS CITY', 
                        'General Santos City (Dadiangas)',
                        'GENERAL SANTOS CITY (DADIANGAS)',
                        'Dadiangas',
                        'DADIANGAS']
}

barangay_data = { #source: https://www.citypopulation.de/en/philippines/admin/
    'scope' : 'municipality',
    'general_santos' : {
        'apopong' : {
            'uid'        : 0,
            'population' : 58314,
            'households' : 14580, #all households count are estimates based on mean household size and std of 1.0
            'area'       : 20.52
        },
        'baluan' : {
            'uid'        : 1,
            'population' : 11861,
            'households' : 2966,
            'area'       : 11.95
        },
        'batomelong' : {
            'uid'        : 2,
            'population' : 2967,
            'households' : 745,
            'area'       : 5.154
        },
        'buayan'    : {
            'uid'        : 3,
            'population' : 11487,
            'households' : 2872,
            'area'       : 4.780
        },
        'bula' :{
            'uid'        : 4,
            'population' : 30845,
            'households' : 7712,
            'area'       : 2.993
        },
        'calumpang' :{
            'uid'        : 5,
            'population' : 87718,
            'households' : 21930,
            'area'       : 8.868
        },
        'city heights' :{
            'uid'        : 6,
            'population' : 24343,
            'households' : 6086,
            'area'       : 4.819
        },
        'conel' :{
            'uid'        : 7,
            'population' : 15931,
            'households' : 3983,
            'area'       : 51.99
        },
        'dadiangas east (pob.)' :{
            'uid'        : 8,
            'population' : 3387,
            'households' : 847,
            'area'       : 0.6122
        },
        'dadiangas north':{
            'uid'        : 9,
            'population' : 6801,
            'households' : 1701,
            'area'       : 0.9629
        },
        'dadiangas south' :{
            'uid'        : 10,
            'population' : 4815,
            'households' : 1204,
            'area'       : 0.6262
        },
        'dadiangas west' :{
            'uid'        : 11,
            'population' : 13090,
            'households' : 3273,
            'area'       : 0.8390
        },
        'fatima' : {
            'uid'        : 12,
            'population' : 72613,
            'households' : 18154,
            'area'       : 22.66
        },
        'katangawan' :{
            'uid'        : 13,
            'population' : 17355,
            'households' : 4339,
            'area'       : 19.64
        },
        'labangal' : {
            'uid'        : 14,
            'population' : 77052,
            'households' : 19263,
            'area'       : 9.494
        },
        'lagao (1st & 3rd)' :{
            'uid'        : 15,
            'population' : 53706,
            'households' : 13427,
            'area'       : 11.95
        },
        'ligaya' : {
            'uid'        : 16,
            'population' : 6688,
            'households' : 1672,
            'area'       : 6.184
        },
        'mabuhay' :{
            'uid'        : 17,
            'population' : 37629,
            'households' : 9408,
            'area'       : 43.69
        },
        'olympog' :{
            'uid'        : 18,
            'population' : 4455,
            'households' : 1114,
            'area'       : 13.84
        },
        'san isidro (lagao 2nd)' :{
            'uid'        : 19,
            'population' : 64958,
            'households' : 16240,
            'area'       : 14.86
        },
        'san jose' :{
            'uid'        : 20,
            'population' : 13504,
            'households' : 3376,
            'area'       : 60.90
        },
        'siguel' :{
            'uid'        : 21,
            'population' : 15687,
            'households' : 3922,
            'area'       : 36.86
        },
        'sinawal' :{
            'uid'        : 22,
            'population' : 18467,
            'households' : 4617,
            'area'       : 80.65
        },
        'tambler' :{
            'uid'        : 23,
            'population' : 31539,
            'households' : 7885,
            'area'       : 44.37
        },
        'tinagacan' :{
            'uid'        : 24,
            'population' : 8344,
            'households' : 2086,
            'area'       : 24.30
        },
        'upper labay' :{
            'uid'        : 25,
            'population' : 3759,
            'households' : 940,
            'area'       : 17.61
        },
    },
    'banga': {
        'benitez': {
            'uid': 0,
            'population': 3205,
            'households':0,
        }
    }
}

def estimate_households_count():
    
    return
