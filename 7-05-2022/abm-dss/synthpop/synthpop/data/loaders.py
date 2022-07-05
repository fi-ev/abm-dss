import numpy as np

from pandas import read_excel
from pkg_resources import resource_filename

from . import barangay_data         as brgy_data
from . import households_data       as hh_data
from . import establishments_data   as est_data
from . import population_data       as pop_data

def parse_location_names(location = None):
    
    """
    parse location names to valid location key; e.g. ''

    Args:
        location (dict) : location parameter (params['location']). Defaults to None.
        
    Returns:
        boolean: returns False if parsing failed.
        dict   : parsed location names
        
    """
    if location is not None:
        parsed_location = {}
        for loc in location:
            val_loc = location[loc].lower()
            val_loc = val_loc.replace(' ', '_')
            parsed_location[loc] = val_loc
        return parsed_location
    
    return False

def get_all_barangay_data(location = None):
    """
    Get all barangay data from location.
    
    Args:
        location (dict): location parameter (params['location']). Defaults to None.

    Returns:
        dict: all barangay data
    """
    loc       = parse_location_names(location = location)
    scope     = brgy_data.barangay_data['scope']
    location  = loc[scope]
    
    all_brgy_data = brgy_data.barangay_data[location]
    
    return all_brgy_data

def get_sex_data(location = None):
    """
    Get sexes data from location.

    Args:
        location (dict): location parameter (params['location']). Defaults to None.

    Returns:
        ndarray: array of population sex distribution percentages by age
    """
    
    loc       = parse_location_names(location = location)
    scope     = pop_data.population_sex_data['scope']
    location  = loc[scope]
    
    #access data: the actual data and the total
    sex_data = pop_data.population_sex_data[location]['males,females']
    total    = pop_data.population_sex_data[location]['total']
    total = total[0] + total[1]
    #get the length of the data
    length = len(sex_data.keys())
    
    #initialize empty ndarrays of size length
    mins    = np.empty(length, dtype = np.int32)
    maxs    = np.empty(length, dtype = np.int32)
    males   = np.empty(length, dtype = np.float32)
    females = np.empty(length, dtype = np.float32)

    #loop through the data and do some data manipulation
    for i,key in enumerate(sex_data.keys()):
        ranges  = key.split('-')
        mins[i] = int(ranges[0])
        maxs[i] = int(ranges[1])
        
        p = sex_data[key][0] / total
        males[i] = p
        
        p = sex_data[key][1] / total
        females[i] = p
    
    #initialize     
    sexes = np.empty((length, 4), dtype = object)
    
    sexes[:,0] = mins
    sexes[:,1] = maxs
    sexes[:,2] = males
    sexes[:,3] = females
    
    return sexes


def get_age_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = pop_data.population_age_data['scope']
    location  = loc[scope]
    
    #access data: the actual data and the total
    age_data = pop_data.population_age_data[location]['ages']
    total    = pop_data.population_age_data[location]['total']
            
    #get the length of the data
    length = len(age_data.keys())
    
    mins    = np.empty(length, dtype = np.int32)
    maxs    = np.empty(length, dtype = np.int32)
    probs   = np.empty(length, dtype = np.float32)
    
    #loop through the data and do some data manipulation
    for i,key in enumerate(age_data.keys()):
        ranges  = key.split('-')
        mins[i] = int(ranges[0])
        maxs[i] = int(ranges[1])
        
        p = age_data[key] / total
        probs[i] = p

    #initialize ndarray for finalization 
    ages = np.empty((length,3), dtype=object)
    
    ages[:,0] = mins
    ages[:,1] = maxs
    ages[:,2] = probs
    
    return ages

def get_households_avg_size_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = hh_data.household_avg_size['scope']
    location  = loc[scope]
    
    avg_household_size = hh_data.household_avg_size[location]
    
    return avg_household_size

def get_household_size_members_by_age_group(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = hh_data.household_avg_size['scope']
    location  = loc[scope]
    
    household_size_members_by_age_group = hh_data.household_members_by_age_group[location]['age_groups']
    #total = hh_data.household_members_by_age_group[location]['total']
    
    length = len(household_size_members_by_age_group.keys())
    
    mins = np.empty(length, dtype = np.int32)
    maxs = np.empty(length, dtype = np.int32)
    probs = []
    
    for i,key in enumerate(household_size_members_by_age_group.keys()):
        ranges = key.split('-')
        mins[i] = int(ranges[0])
        maxs[i] = int(ranges[1])
        
        #TODO: calculate probabilities here since we'll be using raw data
        probs.append(household_size_members_by_age_group[key])
    
    probs = np.array(probs)
    household_size_members = np.empty((length, 10), dtype = object)
    
    for i in range(10):
        if   i == 0:
            household_size_members[:,i] = mins
        elif i == 1:
            household_size_members[:,i] = maxs
        else:
            household_size_members[:,i] = probs[:,i-2]    
            
    return household_size_members

def get_employment_rate_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = pop_data.population_employment_rate['scope']
    location  = loc[scope]
    
    employment_rate = pop_data.population_employment_rate[location]
    
    return employment_rate

def get_enrollment_rate_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = pop_data.population_enrollment_rate['scope']
    location  = loc[scope]
    
    enrollment_rate = pop_data.population_enrollment_rate[location]
    
    return enrollment_rate

def get_teachers_personnel_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = pop_data.teaching_personnel_count['scope']
    location  = loc[scope]
    
    teaching_count         = pop_data.teaching_personnel_count[location]['teaching']['counts']
    #teaching_related_count = pop_data.teaching_personnel_count[location]['teaching_related']['counts']
    
    total_teaching_count            = pop_data.teaching_personnel_count[location]['teaching']['total']
    #total_teaching_related_count    = pop_data.teaching_personnel_count[location]['teaching_related']['total']
    
    teaching_personnel_rate = (teaching_count / total_teaching_count) #+ (teaching_related_count / total_teaching_related_count)

    return teaching_personnel_rate

def get_teachers_ratio_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = pop_data.teaching_personnel_count['scope']
    location  = loc[scope]
    
    teaching_ratio = pop_data.teacher_student_ratio[location]
    
    return teaching_ratio

def get_non_teaching_rate_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = pop_data.non_teaching_personnel_count['scope']
    location  = loc[scope]
    
    non_teaching_count = pop_data.non_teaching_personnel_count[location]['non_teaching']['counts']
    total              = pop_data.non_teaching_personnel_count[location]['non_teaching']['total']
    
    non_teaching_rate = non_teaching_count / total
    
    return non_teaching_rate

def get_total_number_of_establishments_data(location  = None):
    loc       = parse_location_names(location = location)
    scope     = est_data.number_of_establishments['scope']
    location  = loc[scope]
    
    total_establishments = est_data.number_of_establishments[location]['total']
    
    return total_establishments

def get_establishments_employee_sizes_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = est_data.number_of_establishments['scope']
    location  = loc[scope]
    
    establishments_employee_sizes = est_data.number_of_establishments[location]['employees_size']
    
    length = len(establishments_employee_sizes.keys())
    
    mins    = np.empty(length, dtype = np.int32)
    maxs    = np.empty(length, dtype = np.int32)
    counts  = np.empty(length, dtype = np.int32)
    
    for i,key in enumerate(establishments_employee_sizes.keys()):
        ranges  = key.split('-')
        mins[i] = int(ranges[0])
        maxs[i] = int(ranges[1])
        counts[i] = establishments_employee_sizes[key]
    
    employee_sizes = np.empty((length,3),dtype = np.int32)
    employee_sizes[:,0] = mins
    employee_sizes[:,1] = maxs
    employee_sizes[:,2] = counts
    
    return employee_sizes
    
def get_establishments_industries_data(location = None):
    
    loc       = parse_location_names(location = location)
    scope     = est_data.establishments_industries_data['scope']
    location  = loc[scope]
    
    industries_data = est_data.establishments_industries_data[location]
    total           = industries_data['total']
    industries      = industries_data['industries']
    
    length = len(industries.keys())
    k      = list(industries.keys())
    column = len(industries[k[0]]) + 2 #+ 2 for mins and maxs

    mins = np.empty(length,  dtype = np.int32)
    maxs = np.empty(length,  dtype = np.int32)
    industries_probs = np.empty((length, column), dtype = object)
    
    for i,key in enumerate(industries.keys()):
        ranges  = key.split('-')
        mins[i] = ranges[0]
        maxs[i] = ranges[1]
        
        industries_arr = np.array(industries[key])
        
        probabilities = industries_arr / total[key]
                        #row, column
        industries_probs[i:i+1,2:] = probabilities
    
    industries_probs[:,0] = mins
    industries_probs[:,1] = maxs
    
    return industries_probs

def load_schools(location = None):
    loc       = parse_location_names(location = location)
    names     = brgy_data.municipality_aliases[loc['municipality']]
    
    filepath = resource_filename('synthpop','data/xlsx/schools.xlsx')
    
    data = read_excel(filepath)
    
    result = data.loc[data['Municipality'].isin(names)]
    
    school_name         = result['School Name']
    barangay            = result['Barangay']
    classification      = result['Urban/Rural Classification']
    curriculum          = result['Modified Curricural Offering Classification']
    
    json_data = {
        'names':             [ school_name[i]        for i in range(len(school_name))],
        'barangay':         [ barangay[i].lower()   for i in range(len(barangay))],
        #'classification':  [ classification[i]     for i in range(len(classification))],
        'curriculum':       [ curriculum[i]         for i in range(len(curriculum))]
    }
    
    return json_data

def load_colleges(location = None):
    
    loc       = parse_location_names(location = location)
    names     = brgy_data.municipality_aliases[loc['municipality']]
    
    filepath = resource_filename('synthpop','data/xlsx/colleges.xlsx')
    
    data = read_excel(filepath)
    
    result = data.loc[data['Municipality'].isin(names)]
    
        
    college_name = result['Institution Name']
    #TODO: change this to the actual barangay data is done
    barangay_names = list(brgy_data.barangay_data[loc['municipality']].keys())
    barangay     = np.random.choice(barangay_names, len(college_name))
    
    
    json_data = {
        'names':              [ college_name[key] for key in college_name.keys()],
        'barangay':          barangay,
        'curriculum':        ['college' for i in range(len(college_name.keys()))]
    }
    
    return json_data


def load_hcfacilities(location = None):
    
    loc       = parse_location_names(location = location)
    names     = brgy_data.municipality_aliases[loc['municipality']]
    
    filepath = resource_filename('synthpop','data/xlsx/hcfacilities.xlsx')
    
    data = read_excel(filepath)
    
    result = data.loc[data['City/Municipality Name'].isin(names)]
    
    hcfacility_name     = result['Facility Name']
    hcfacility_type     = result['Health Facility Type']
    barangay            = result['Barangay Name']
    service_capability  = result['Service Capability']
    bed_capacity        = result['Bed Capacity']
    
    json_data = {
        'name'               : [hcfacility_name[key].lower() for key in hcfacility_name.keys()],
        'type'               : [hcfacility_type[key].lower() for key in hcfacility_type.keys()],
        'barangay'           : [barangay[key].lower() for key in barangay.keys()],
        'service_capability' : [service_capability[key] if isinstance(service_capability[key], str) else '' for key in service_capability.keys()],
        'bed_capacity'       : [0.0 if np.isnan(bed_capacity[key]) else bed_capacity[key] for key in bed_capacity.keys()]
    }
    
    
    return json_data
    
    