import numpy as np
import defaults as df

from . import data

def initialize_households(parameters = None, barangay_dict = None):
    
    """
    Initialize households.
        
    Args:
        parameters (dict)      : parameter settings
        barangay_dict (dict)   : dictionary of initial barangay properties
        
    Returns:
        dict of list: 
            uids              : unique id
            barangay_uid      : unique id of the barangay this household belongs to
            size              : size of the household
    
     Data:
        barangay_data (source: https://www.citypopulation.de/en/philippines/admin/)
        
    """
    
    print(f'Initializing households. . .')
    
    
    barangay_data = data.get_all_barangay_data(parameters['location'])
    
    barangays = barangay_data.keys()
    n_barangays = len(barangays)

    households_count_per_barangay = np.empty(n_barangays, dtype = df.d_integer)
    
    for i,brgy in enumerate(barangays):
        households_count_per_barangay[i] = barangay_data[brgy]['households']

    households_count = np.cumsum(households_count_per_barangay)[-1]
    
    uid             = np.arange(households_count, dtype = np.int32)
    sizes           = create_household_sizes(parameters, barangay_dict)
    barangay_uid    = assign_barangay_uid(barangay_dict)
    #members         = assign_household_members(parameters, sizes, population_dict)
    
    households_dict = {}
    households_dict['uid']              = uid
    households_dict['sizes']            = sizes
    households_dict['barangay_uid']     = barangay_uid

    return households_dict

def assign_barangay_uid(barangay_dict = None):
    
    households_count_per_brgy = barangay_dict['households']
    
    barangay_uid = []
    for i,counts in enumerate(households_count_per_brgy):
        barangay_uid.extend(np.full(counts, i, dtype = np.int32))
    
    return barangay_uid

def create_household_sizes(parameters = None, barangay_dict = None):
    
    #average household size from data
    avg_household_size = data.get_households_avg_size_data(parameters['location'])
    
    #get households count per barangay and population count per barangay from barangay_dict
    households_count_per_brgy = barangay_dict['households']
    population_count_per_brgy = barangay_dict['population']
    
    sizes = []
    for i,counts in enumerate(households_count_per_brgy):
        size = df.rng.normal(avg_household_size, 1.0, counts)
        size = np.abs(np.round(size))
        size = np.array(size, dtype=np.int32)
        
        init_total = np.sum(size)
        
        if(init_total < population_count_per_brgy[i]):
            offset = population_count_per_brgy[i] - init_total
            
            indices_to_add = df.rng.choice(len(size), offset, replace = False)
            size[indices_to_add] += 1
            
        elif(init_total > population_count_per_brgy[i]):
            offset = init_total - population_count_per_brgy[i]
            
            non_one_indices = np.where(size > 2)[0]
            
            indices_to_reduce = df.rng.choice(non_one_indices, offset, replace = False)
            size[indices_to_reduce] -= 1

        sizes.extend(size)
    
    return sizes

def assign_household_members(parameters = None, households_init = None, population_dict = None):
    
    sizes = households_init['sizes']
    
    household_size_members_by_age_group = data.get_household_size_members_by_age_group(parameters['location'])
    mins = household_size_members_by_age_group[:,0]
    maxs = household_size_members_by_age_group[:,1]
    probs = household_size_members_by_age_group[:,2:]

    probs = np.array(probs, dtype = np.float64)

    ages = population_dict['ages']
    uid  = population_dict['uid']
    
    #first, group/bin population by age
    age_bins = {}
    for i in range(len(mins)):
        age_indices = np.where(np.logical_and(ages >= mins[i], ages <= maxs[i]))[0]
        age_bins[i] = list(uid[age_indices])
        
        mask = np.ones(len(ages), dtype=bool)
        mask[age_indices] = False
        ages = ages[mask,...]
        
        mask = np.ones(len(uid), dtype = bool)
        mask[age_indices] = False
        uid = uid[mask,...]

    household_members = {}
    for i,size in enumerate(sizes):
        
        household_members[i] = []
        
        if(size == 0):
            continue
        
        column = size
        if(column >= 8):
            column = 7
        
        available_bins = list(age_bins.keys())  

        p = probs[:,column]   
        p = p[available_bins]
        p /= p.sum()
        
        member_bins = df.rng.choice(a = available_bins, size = size, p = p)
        
        for idx,member_bin in enumerate(member_bins):
            
            if member_bin in age_bins:
                uid = age_bins[member_bin].pop()
                
                if len(age_bins[member_bin]) == 0:
                    del age_bins[member_bin]
            else:
                available_bins = list(age_bins.keys())  

                p = probs[:,column]   
                p = p[available_bins]
                p /= p.sum()
                
                new_member_bin = int(df.rng.choice(a = available_bins, size = 1, p = p))
                
                uid = age_bins[new_member_bin].pop()
            
            household_members[i].append(uid)
    
    return household_members

def create_households(household_init, household_members):
    
    households = []
    
    households_count = len(household_init['uid'])
    
    for i in range(households_count):
        uid             = household_init['uid'][i]
        size            = household_init['sizes'][i]
        barangay_uid    = household_init['barangay_uid'][i]
        members         = household_members[i]
        
        households.append(Household(uid = uid, size = size, barangay_uid = barangay_uid, members = members))
    
    return households

def create_households_dict(household_init, household_members):
    
    households_dict = {}
    
    n_households = len(household_init['uid'])
    households_dict['uid'] = []
    households_dict['barangay_uid'] = []
    households_dict['members'] = []
    
    for i in range(n_households):
        uid             = household_init['uid'][i]
        barangay_uid    = household_init['barangay_uid'][i]
        members         = household_members[i]
        
        households_dict['uid'].append(uid)
        households_dict['barangay_uid'].append(barangay_uid)
        households_dict['members'].append(members)
        
    return households_dict

def get_available_keys():
    keys = ['uid', 'barangay_uid', 'members']
    return keys

class Household():
    def __init__(self, uid, size, barangay_uid, members):
        self.uid = uid
        self.size = size
        self.barangay_uid = barangay_uid
        self.members = members
        return
    
    def __repr__(self):
        return f'HOUSEHOLD WITH: \n\t UID: {self.uid} \n\t SIZE: {self.size} \n\t BARANGAY UID: {self.barangay_uid} \n\t MEMBERS: {self.members}'