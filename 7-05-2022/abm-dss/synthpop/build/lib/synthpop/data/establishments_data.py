number_of_establishments = { #source: (2019) https://onedrive.live.com/view.aspx?resid=9CD3CF10466EFD3A!1640&ithint=file%2cxlsx&authkey=!AHhicsAgoFjxveA 
    'scope': 'municipality', #excludes sari-sari stores with no paid employees, retail sale via stalls and markets, activities of membership organizations, and public health and education services establishments."
    'general_santos' : {
        'total'   : 8826,
        'employees_size':{
            '1-9'     : 7755,
            '10-99'   : 983,
            '100-199' : 49,
            '200-299' : 39
        }
        
    }
}

establishments_industries_data = {
    'scope': 'region',
    'soccsksargen': {
        'total' : {
            'all'       : 44876,
            '1-9'       : 41714,
            '10-99'     : 2935,
            '100-199'   : 125,
            '200-299'   : 102
        },
        'industries':{
            '1-9'       : [233,24,4761,22,43,65,21668,218,6640,1190,1601,185,541,587,311,835,697,2093],
            '10-99'     : [129,9,289,20,25,35,1086,64,446,44,238,27,9,22,282,93,37,80],
            '100-199'   : [21,0,19,1,2,5,23,1,3,0,6,0,3,5,19,17,0,0],
            '200-299'   : [19, 1, 7, 6, 2, 2, 14, 2, 1, 0, 4, 0, 0, 24, 7, 13,0,0],
        }
        
    }
}
