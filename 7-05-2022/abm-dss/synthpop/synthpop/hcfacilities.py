import numpy as np

from . import data

def initialize_hcfacility(parameters, barangay_init):
    
    print(f'Initializing healthcare facilities . . . ')
    
    hcfacilities = data.load_hcfacilities(parameters['location'])

    n_hcf = len(hcfacilities['name'])
    hcfacilities['uid']          = np.arange(n_hcf)
    hcfacilities['barangay_uid'] = map_brgy_name_to_brgy_uid(hcfacilities['barangay'], barangay_init)
    
    
    return hcfacilities 

def map_brgy_name_to_brgy_uid(barangays, barangay_init):
    
   barangay_init_names = barangay_init['names']
   barangay_init_uid   = barangay_init['uid']
    
   dict_barangay_init = dict(zip(barangay_init_names, barangay_init_uid))

   uids = [dict_barangay_init[barangay] for i,barangay in enumerate(barangays)]
    
   return uids

def create_hcfacilities_dict(hcf_init):
    
    #TODO: create hcfacilities 
    hcfacilities_dict = {}
    hcfacilities_dict['uid']                    = hcf_init['uid']
    hcfacilities_dict['names']                  = hcf_init['name']
    hcfacilities_dict['barangay_uid']           = hcf_init['barangay_uid']
    hcfacilities_dict['service_capability']     = hcf_init['service_capability']
    hcfacilities_dict['bed_capacity']           = hcf_init['bed_capacity']
    
    return hcfacilities_dict

def get_available_keys():
    keys = ['uid', 'names', 'barangay_uid', 'service_capability', 'bed_capacity']
    return keys

class HCFacility():
    def __init__(self):
        return

