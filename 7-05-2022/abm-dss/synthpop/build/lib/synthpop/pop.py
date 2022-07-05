import numpy as np
import defaults as df

from . import data


def initialize_population(parameters = None, barangay_init = None):
    """
    Create initial properties of the population. 
    Initial properties: 
        - uids  - unique ids for each person
        - ages  - age of each person
        - sexes - sex of a person

    Args:
        parameters (dict)       : parameter settings
        barangay_init (dict)    : barangay initial properties
    Returns:
        population_init (dict)  : dictionary of all initial population properties
    """
    print(f'Initializing population. . .')
    population_size = np.cumsum(barangay_init['population'])[-1]
    
    uid   = np.arange(population_size, dtype = np.int32)
    ages  = create_ages(parameters, population_size)
    sexes = assign_sexes(parameters, population_size)
    
    #occ = assign_all_occupations(parameters, uid, ages)
    
    population_init = {}
    population_init['uid']   = uid
    population_init['ages']  = ages
    population_init['sexes'] = sexes
    
    return population_init

def create_ages(parameters, population_size):
    """
    Create ages for the population based on a distribution.

    Args:
        parameters      (dict): parameters dictionary
        population_size  (int): total size of the population

    Returns:
        ndarray : array of integers representing population ages with length population_size
        
    Data:
        ages data
        
    """
    ages_data = data.get_age_data(parameters['location'])
    
    mins   = ages_data[:,0]
    maxs   = ages_data[:,1]
    ranges = maxs - mins
    
    p = np.array(ages_data[0:,2], dtype = np.float64)
    
    p/=p.sum()
    
    ages = np.empty(population_size)
    
    bins = df.rng.choice(a = np.arange(len(p)), size = population_size, p = p)
    
    ages = mins[bins] + ranges[bins] * df.rng.random(size=population_size) #np.random.random(size = population_size)

    ages = list(map(round,ages))
    
    ages = np.array(ages)
    
    return ages

def assign_sexes(parameters, population_size):
    """
    Assign sexes to population based on a binomial distribution.
    Note: 1 - males ; 0 - females
    
    Args:
        parameters      (dict)  : parameters dictionary
        population_size (int)   : total size of the population

    Returns:
        ndarray: array of integers representing population sexes of size population_size
        
    Data:
        sexes data
    """
    sexes_data = data.get_sex_data(parameters['location'])
    
    p_males = sexes_data[:,2]

    #males = 1; females = 0
    sexes = df.rng.binomial(n = 1, p = p_males.sum(), size = population_size)
    
    return sexes

def get_students(parameters, uid, ages):
    """
    
    Assign a number of students through simple random sampling. 
    Possible students are those population with ages 5 - 25.
    
    Args:
        parameters  (dict)   : parameters dictionary
        uid         (ndarray): array of population uids
        ages        (ndarray): array of population ages

    Returns:
        tuple of dictionaries: 
            dict: assigned students
            dict: population leftover
    
    Data:
        enrollment_rate_data
        defaults: 
        
    """
    enrollment_rate_data = data.get_enrollment_rate_data(parameters['location'])
    school_age_brackets  = data.school_curriculum_age_brackets
    
    students_uids = []
    students_ages = []
    
    for key in school_age_brackets.keys():
        mins, maxs  = school_age_brackets[key]
        age_indices = np.where(np.logical_and(ages >= mins, ages <= maxs))[0]
        
        enrollment_rate = enrollment_rate_data[key]
        probs = [1 - enrollment_rate, enrollment_rate]
        
        choose_enrolled = df.rng.choice(a = np.arange(len(probs)), size = len(age_indices), p = probs)
        enrolled = np.where(choose_enrolled == 1)[0]
        enrolled_age_indices = age_indices[enrolled]

        students_uids.extend(uid[enrolled_age_indices])
        students_ages.extend(ages[enrolled_age_indices])
        
        mask = np.ones(len(ages), dtype = bool)
        mask[enrolled_age_indices] = False
        
        ages = ages[mask,...]
        uid  = uid[mask,...]
        
    students = {}
    students['uid']  = np.array(students_uids)
    students['ages'] = np.array(students_ages)
    
    population_left_to_assign = {}
    population_left_to_assign['uid'] = uid
    population_left_to_assign['ages'] = ages
        
    return (students, population_left_to_assign)

def get_employed(parameters, uid, ages):
    
    employment_rate_data = data.get_employment_rate_data(parameters['location'])
    age_indices = np.where(ages >= 15)[0]
    
    employment_rate    = [1-employment_rate_data, employment_rate_data]
    employed_indices   = df.rng.choice(a = np.arange(len(employment_rate)), size = len(age_indices), p = employment_rate)

    employed_indices   = np.where(employed_indices == 1)[0]
    
    employed = {}
    employed['ages']    = np.array(ages[employed_indices])
    employed['uid']     = np.array(uid[employed_indices])
    
    unemployed = {}
    mask = np.ones(uid.size, dtype = bool)
    mask[employed_indices] = False
    
    unemployed['uid']  = uid[mask]
    unemployed['ages'] = ages[mask]
    
    unemp = len(unemployed['uid'])
    
    return (employed, unemployed)

def get_teachers(parameters, uid, ages):
    
    teachers_percentage = data.get_teachers_personnel_data(parameters['location'])
    
    age_indices = np.where(np.logical_and(ages >= 18, ages <= 65))[0]

    teachers_n_rate = [1 - teachers_percentage, teachers_percentage]
    teachers_indices = df.rng.choice(a = np.arange(len(teachers_n_rate)), size = len(age_indices), p = teachers_n_rate)
    teaching_indices = np.where(teachers_indices == 1)[0]
    
    teachers = {}
    teachers['ages'] = ages[teaching_indices]
    teachers['uid']  = uid[teaching_indices]
    
    employed_left = {}
    mask = np.ones(uid.size, dtype = bool)
    mask[teaching_indices] = False
    employed_left['uid'] = uid[mask]
    employed_left['ages'] = ages[mask]

    
    return (teachers, employed_left)

def get_school_staff(parameters, uid, ages):
    
    non_teaching_rate = data.get_non_teaching_rate_data(parameters['location'])
    
    non_teaching_probs = [1-non_teaching_rate, non_teaching_rate]
    non_teaching_indices = df.rng.choice(a = np.arange(len(non_teaching_probs)), size = len(uid), p = non_teaching_probs)
    
    staff_indices    = np.where(non_teaching_indices == 1)[0]
    
    staff = {}
    staff['uid'] = uid[staff_indices]
    staff['ages'] = ages[staff_indices]
    
    employed_left = {}
    mask = np.ones(uid.size, dtype = bool)
    mask[staff_indices] = False
    
    employed_left['uid']  = uid[mask]
    employed_left['ages'] = ages[mask]
    
    return (staff, employed_left)

def get_establishment_employees(establishments_init, uid, ages):
    
    establishment_sizes = establishments_init['sizes']
    
    sizes_sum = sum(establishment_sizes)
    
    employees_indices = df.rng.choice(np.arange(len(uid)), sizes_sum)
    
    employees_uid  = uid[employees_indices]
    employees_ages = ages[employees_indices]

    establishment_employees = {}
    establishment_employees['uid']  = employees_uid
    establishment_employees['ages'] = employees_ages
    
    employed_left = {}
    mask = np.ones(uid.size, dtype = bool)
    mask[employees_indices] = False
    employed_left['uid']  = uid[mask]
    employed_left['ages'] = uid[ages]
    
    return (establishment_employees, employed_left)

def create_population(population_init, households_list, schools_list, establishments_list):
    
    '''
        NOTE: Uses Class
    '''
    pop = {}
    
    n_pop = len(population_init['uid'])
    
    pop['uid']   = []
    pop['ages']  = []
    pop['sexes'] = []
    for i in range(n_pop):
        pop['uid'].append(population_init['uid'][i])
        pop['ages'].append(population_init['ages'][i])
        pop['sexes'].append(population_init['sexes'][i])
        
    households_id = np.empty(len(pop['uid']), dtype = np.int32)
    barangay_id   = np.empty(len(pop['uid']), dtype = np.int32)
    for hh in households_list:
        hh_barangay = hh.barangay_uid
        for member in hh.members:
            households_id[member] = hh.uid
            barangay_id[member]   = hh_barangay
            
    schools_id = np.full(len(pop['uid']), -1, dtype = np.int32)
    
    for sch in schools_list:
        for student in sch.all_students:
            schools_id[student] = sch.uid
        for teacher in sch.teachers:
            schools_id[teacher] = sch.uid
        for staff in sch.staff:
            schools_id[staff] = sch.uid
    
    establishments_id = np.full(len(pop['uid']), -1, dtype = np.int32)
    
    for est in establishments_list:
        for employee in est.employees:
            establishments_id[employee] = est.uid
    
    pop['barangay']         = barangay_id
    pop['household']        = households_id
    pop['school']           = schools_id
    pop['establishment']    = establishments_id
    
    #pop['location']['barangay']
    #pop['location']['household']
    #pop['location']['establishment']
    #pop['location']['school']
    #pop['location']['church']
    #pop['location']['other']
    
    #pop['property']['uid']
    #pop['property']['sex']
    #pop['property']['age']
    
    #pop['uid']['contacts'] = { ['household']['community']['workplace']['school'] }
    
    return pop
