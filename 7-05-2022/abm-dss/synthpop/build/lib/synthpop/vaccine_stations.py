import defaults as df

def initialize_vaccine_stations(params, brgy_init):
    
    n_vax = params['vaccine_stations']
    brgy_uid = brgy_init['uid']
    
    vax_init = {}
    vax_init['barangay_uid']    = df.rng.choice(brgy_uid, size = n_vax)
    
    return vax_init