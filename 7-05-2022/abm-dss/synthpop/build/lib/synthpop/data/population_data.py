population_age_data = { # source: https://psa.gov.ph/content/census-population-and-housing-report
    'scope' : 'municipality',
    'general_santos':{
        'total'     : 592884,
        'ages' :{
                '0-1'       : 14386,
                '1-4'       : 54462,
                '5-9'       : 60353,
                '10-14'     : 58039,
                '15-19'     : 61769,
                '20-24'     : 60642,
                '25-29'     : 53191,
                '30-34'     : 44993,
                '35-39'     : 40457,
                '40-44'     : 35633,
                '45-49'     : 31367,
                '50-54'     : 24851,
                '55-59'     : 19077,
                '60-64'     : 13884,
                '65-69'     : 8674,
                '70-74'     : 5018,
                '75-79'     : 3365,
                '80-99'     : 2723,
        }
    },
}

population_sex_data = { #source: https://psa.gov.ph/content/census-population-and-housing-report
    'scope': 'municipality',
    'general_santos': {
        'total'     :   [299899, 294547 ],
        'males,females':{
            '0-1'       :  [7462,   6937   ],
            '1-4'       :  [27779,  26690  ],
            '5-9'       :  [31038,  29340  ],
            '10-14'     :  [29393,  28708  ],
            '15-19'     :  [30606,  31322  ],
            '20-24'     :  [30388,  30521  ],
            '25-29'     :  [27260,  26181  ],
            '30-34'     :  [23283,  21888  ],
            '35-39'     :  [20961,  19680  ],
            '40-44'     :  [18296,  17466  ],
            '45-49'     :  [15870,  15609  ],
            '50-54'     :  [12575,  12351  ],
            '55-59'     :  [9385,   9725   ],
            '60-64'     :  [6879,   7023   ],
            '65-69'     :  [4065,   4625   ],
            '70-74'     :  [2233,   2798   ],
            '75-79'     :  [1402,   1969   ],
            '80-99'     :  [1024,   1714   ]
        },
    }
}

population_employment_rate = { #source: Table 1. Provincial Total Employed persons and Employment Rate 2018, 2019, 2020 (2019) https://psa.gov.ph/content/annual-provincial-labor-market-statistics-final-results
    'scope': 'region',
    'soccsksargen': 0.956
}

population_enrollment_rate = { #source: PSA https://psa.gov.ph/products-and-services/publications/philippine-statistical-yearbook (Chapter 10)
    'scope': 'region',
    'soccsksargen': {
            'kindergarten'    : 0.7600,         #PSA
            'primary'         : 0.9204,         #PSA
            'junior'          : 0.7449,         #PSA
            'senior'          : 0.4150,         #PSA
            'college'         : 0.0311,         #CHED (source): https://ched.gov.ph/statistics/ ; NOTE: this is philippines as a whole since no data is available by region;
    }
}

teaching_personnel_count = {
    'scope': 'region',
    'soccsksargen': {
        'teaching':{
            'counts'   :     40717,
            'total'    :     805957,
        },
        'teaching_related' : {
            'counts'   :     1907,
            'total'   :      43129
        }  
        
    }
}

non_teaching_personnel_count = {
    'scope': 'region',
    'soccsksargen': {
        'non_teaching':{
            'counts'   :     2484,
            'total'    :     53539
        },
        'authorized_personnel' : {
            'counts'    :     45108,
            'total'     :     902625
        }
    }
}