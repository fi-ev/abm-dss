import numpy as  np
import defaults as df

from . import data

def initialize_barangay(parameters):
    """
    Initialize barangay.

    Args:
        parameters (dict): parameters dictionary

    Returns:
        dict of list:   
                uid               : list of barangay uids
                names             : list of barangay names
                population_count  : list of population count for each barangay 
                households        : list of households count for each barangay
    
     Data:
        barangay_data (source: https://www.citypopulation.de/en/philippines/admin/)
        
    """
    #get barangay data
    barangay_data = data.get_all_barangay_data(parameters['location'])
    
    #get number of barangays
    barangays = barangay_data.keys()
    n_barangays = len(barangays)
    
    #declare empty numpy integer arrays 
    names      = []
    uids       = np.empty(n_barangays, dtype = df.d_integer)
    population = np.empty(n_barangays, dtype = df.d_integer)
    households = np.empty(n_barangays, dtype = df.d_integer)
    
    #assign barangay data to their respective arrays
    for i,brgy in enumerate(barangays):
        uids[i]         = barangay_data[brgy]['uid']                        
        population[i]   = barangay_data[brgy]['population']
        households[i]   = barangay_data[brgy]['households']
        names.append(brgy) 
    
    #store the arrays to their respective dictionary keys
    barangay_init = {}
    
    barangay_init['uid']       = uids
    barangay_init['names']      = names
    barangay_init['population'] = population
    barangay_init['households'] = households
    
    return barangay_init

def create_barangay(barangay_init, household_init, schools_init):
    """
    
    Create and finalize barangay list of classes

    Args:
        barangay_init  (dict): initialized barangay data dictionary
        household_init (dict): intiialized households data dictionary
        schools_init   (dict): initialized schools data dictionary
    
    Returns:
        list: list of barangay classes with properties
        
    Data:
        n/a
        
    """
    
    #number of barangays
    n_brgys             = len(barangay_init['uid'])
    
    #unpacking dictionary and storing to variables
    households_uid      = np.array(household_init['uid'])
    households_brgy_uid = np.array(household_init['barangay_uid'])
    schools_uid         = np.array(schools_init['uid'])
    schools_brgy_uid    = np.array(schools_init['barangay_uid'])

    #declare empty barangays list
    barangays = []
    
    for i in range(n_brgys):
        uid  = barangay_init['uid'][i]                          #assign uid
        name = barangay_init['names'][i]                        #assign name
        population_count = barangay_init['population'][i]       #assign population count
        
        hh_indices = np.where(households_brgy_uid == uid)[0]    #find indices of households with barangay uid
        hh_uid = households_uid[hh_indices]                     #assign households
        
        sch_indices = np.where(schools_brgy_uid   == uid)[0]    #find indices of schools with barangay uid
        sch_uid     = schools_uid[sch_indices]                  #assign schools
        
        #create a new instance of Barangay with properties and append to list
        barangays.append(Barangay(uid              = uid,
                                  name             = name,
                                  population_count = population_count,
                                  households        = hh_uid,
                                  schools           = sch_uid))
    return barangays

def create_barangays_dict(barangay_init, household_init, schools_init):
    """
    Create and finalize barangay data dictionary 

    Args:
        barangay_init  (dict): initialized barangay data dictionary
        household_init (dict): intiialized households data dictionary
        schools_init   (dict): initialized schools data dictionary

    Returns:
        dict: dictionary of all barangay properties
        
    Data: 
        n/a
    """
    
    #number of barangays
    n_brgys = len(barangay_init['uid'])
    
    #unpacking dictionary and storing to variables
    households_uid      = np.array(household_init['uid'])
    households_brgy_uid = np.array(household_init['barangay_uid'])
    schools_uid         = np.array(schools_init['uid'])
    schools_brgy_uid    = np.array(schools_init['barangay_uid'])
    
    #declaring empty array for every dictionary key
    barangays_dict = {}
    
    barangays_dict['uid']              = []
    barangays_dict['name']             = []
    barangays_dict['population_count'] = []
    barangays_dict['households']       = []
    barangays_dict['schools']          = []
    
    for i in range(n_brgys):
        uid  = barangay_init['uid'][i]                          #assign uid
        name = barangay_init['names'][i]                        #assign name
        population_count = barangay_init['population'][i]       #assign population count
        
        hh_indices = np.where(households_brgy_uid == uid)[0]    #find indices of households with barangay uid
        hh_uid = households_uid[hh_indices]                     #assign households
        
        sch_indices = np.where(schools_brgy_uid   == uid)[0]    #find indices of schools with barangay uid
        sch_uid     = schools_uid[sch_indices]                  #assign schools
        
        #append everything to respective keys in the dictionary
        barangays_dict['uid'].append(uid)                    
        barangays_dict['name'].append(name)
        barangays_dict['population_count'].append(population_count)
        barangays_dict['households'].append(hh_uid)
        barangays_dict['schools'].append(sch_uid)
        
    return barangays_dict
        
def get_available_keys():
    """
    
    Return a list of all finalized barangay properties.

    Returns:
        list: list of all barangay properties.
        
    """
    keys = ['uid', 'names', 'population_count', 'households', 'schools']
    
    return keys

#Barangay class
class Barangay():
    def __init__(self, uid, name, population_count, households, schools):
        self.uid = uid
        self.name = name
        self.population_count = population_count
        self.households = households
        self.schools = schools
        return
    
    def __repr__(self):
        return f'BARANGAY {self.uid}: \n\t NAME: {self.name} \n\t POPULATION COUNT: {self.population_count}\n'
