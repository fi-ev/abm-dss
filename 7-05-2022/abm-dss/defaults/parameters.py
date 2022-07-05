import numpy as np

covid_params                = dict(
    
    location                = dict(
        region              = 'SOCCSKSARGEN',                          #should be from user data. which region they belong to. restricted to region       
        province            = 'South Cotabato',                        #user set. which province
        municipality        = 'General Santos'                                  #user set. set municipality; setting municipality also gets data on province
    ),
                           
    seed                    = 0,                                       #set seed. 0 for random seed.
    infectious_count        = 1,                                       #population count that's infectious at the start
    days                    = 5,                                       #simulation time
    
    
)

def covid_variants():
    ancestral_strain = 0.2 #assumption
    
    alpha_r = ancestral_strain * (ancestral_strain * np.random.uniform(0.5, 0.7))
    beta_r  = ancestral_strain * (ancestral_strain * np.random.uniform(0.2, 1.15))
    gamma_r = ancestral_strain * (ancestral_strain * np.random.uniform(0.5, 1.61))
    delta_r = ancestral_strain * (ancestral_strain * np.random.uniform(0.5, 0.6))
    omicron_r = ancestral_strain * (ancestral_strain * np.random.uniform())
    
    variants = dict (
        
        alpha = dict (r = alpha_r),
        beta  = dict (r = beta_r),
        gamma = dict(r = gamma_r),
        delta_r = dict(r = delta_r),
        omicron_r = dict(r = omicron_r)
        
    )
    
    return variants