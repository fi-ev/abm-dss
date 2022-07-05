import defaults as df
import numpy as np

from . import data

def initialize_establishments(parameters):
    """
    Initialize establishments. 
        
    Args:
        parameters (dict): parameters dictionary

    Returns:
        dict of list
            uid   : unique id
            sizes : employee sizes
            letter: establishment type letter code
            name  : establishment type name code
    
    Data:
        source: https://onedrive.live.com/view.aspx?resid=9CD3CF10466EFD3A!1640&ithint=file%2cxlsx&authkey=!AHhicsAgoFjxveA 
    """
    
    print(f'Initializing establishments . . .')
   
    total_establishments                                = data.get_total_number_of_establishments_data(parameters['location'])
    employee_sizes                                      = create_employee_sizes(parameters)
    establishment_letter, establishment_name            = assign_industry(parameters, employee_sizes)
    
    establishments_init = {}
    
    establishments_init['uid']      = np.arange(total_establishments, dtype = int)
    establishments_init['sizes']    = employee_sizes
    establishments_init['letter']   = establishment_letter
    establishments_init['name']     = establishment_name

    print(f'    Total number of establishments: {total_establishments}')
    return establishments_init

def create_employee_sizes(parameters):
    """
    Assign employee sizes for every establishment.

    Args:
        parameters (dict): parameters dictionary

    Returns:
        ndarray: array of ints
    
    Data:
        source: https://onedrive.live.com/view.aspx?resid=9CD3CF10466EFD3A!1640&ithint=file%2cxlsx&authkey=!AHhicsAgoFjxveA
    """
    
    #get employee sizes data
    employee_sizes_data        = data.get_establishments_employee_sizes_data(parameters['location'])
    
    mins = employee_sizes_data[:,0]     # minimum range of number of employees
    maxs = employee_sizes_data[:,1]     # maximum range of number of employees
    ranges = maxs-mins                  # range of number of employees
    
    counts = employee_sizes_data[:,2]   # number of establishments within the certain range

    employee_sizes = []
    for i in range(len(counts)):        

        sizes = mins[i] + ranges[i] * df.rng.random(counts[i])  #
        sizes = np.round(sizes)
        sizes = np.array(sizes)
        employee_sizes.extend(sizes)
    
    employee_sizes = np.array(employee_sizes, dtype = int)

    return employee_sizes

def assign_industry(parameters, employee_sizes):
    """
    Assign industry code and name to establishments using random sampling.

    Args:
        parameters         (dict): parameters dictionary.
        employee_sizes  (ndarray): array of establishment sizes

    Returns:
        tuple: 
            list: list of generated industry letters
            list: list of generated industry names
            
    Data:
        source: https://onedrive.live.com/view.aspx?resid=9CD3CF10466EFD3A!1627&ithint=file%2cxlsx&authkey=!AEGDAstAU8g7bO0
    """
    industries_arr = data.get_establishments_industries_data(parameters['location'])
    industry_codes  = data.industry_codes
    
    shp = np.shape(industries_arr)
    
    industry_keys = list(industry_codes.keys())
    letters = np.empty(len(employee_sizes), dtype = '<S1')
    
    for i in range(shp[0]):
        industry = industries_arr[i]
        mins = industry[0]
        maxs = industry[1]
        probs = industry[2:]

        p    = np.array(probs, dtype = df.d_float)
        
        size_indices = np.where((employee_sizes >= mins) & (employee_sizes<= maxs))[0]
        
        assigned_industry_letters = df.rng.choice(industry_keys, len(size_indices), p = p)
        
    
        letters[size_indices] = assigned_industry_letters 

    establishment_industry_letters = [letter.decode('UTF-8') for letter in letters]
        
    establishment_industry_names = [industry_codes[key.decode('UTF-8')] for key in letters]
    
    return establishment_industry_letters, establishment_industry_names

def assign_employees(establishments, establishment_employees):
    
    establishments_uid   = establishments['uid']
    establishments_sizes = list(establishments['sizes'])
    
    employees_uid =  establishment_employees['uid']
    
    employees_assignment = {}
    for uid in establishments_uid:
        employees_assignment[uid] = []
        size = establishments_sizes[uid]
        
        employees = employees_uid[:size]
        employees_assignment[uid] = employees
        
        indices = np.arange(len(employees))
        
        mask = np.ones(employees_uid.size, dtype = bool)
        mask[indices] = False
        employees_uid = employees_uid[mask]

    return employees_assignment

def create_establishments(establishments_init, assigned_establishment_employees):
    
    establishments_count = len(establishments_init['uid'])
    
    establishments = []
    for i in range(establishments_count):
        uid             = establishments_init['uid'][i]
        employee_size   = establishments_init['sizes'][i]
        emp             = assigned_establishment_employees[i]
        industry_letter = establishments_init['letter'][i]
        industry_name   = establishments_init['name'][i]
        
        establishments.append(Establishment(uid             = uid, 
                                            employee_size   = employee_size,
                                            employees       = emp,
                                            industry_letter = industry_letter,
                                            industry_name   = industry_name))
        

    
    return establishments

def create_establishments_dict(establishments_init, assigned_establishment_employees):
    
    n_establishments = len(establishments_init['uid'])
    
    establishments_dict = {}
    establishments_dict['uid'] = []
    establishments_dict['industry_letters'] = []
    establishments_dict['industry_names']   = []
    establishments_dict['employees'] = []
    
    for i in range(n_establishments):
        uid             = establishments_init['uid'][i]
        emp             = assigned_establishment_employees[i]
        industry_letter = establishments_init['letter'][i]
        industry_name   = establishments_init['name'][i]
        
        establishments_dict['uid'].append(uid)
        establishments_dict['industry_names'].append(industry_name)
        establishments_dict['industry_letters'].append(industry_letter)
        establishments_dict['employees'].append(emp)
        
    return establishments_dict


def get_available_keys():
    keys = ['uid', 'industry_names', 'industry_letters', 'employees']
    return keys

class Establishment():
    def __init__(self, uid, employee_size, employees, industry_letter, industry_name):
        self.uid                = uid
        self.employee_size      = employee_size
        self.employees          = employees
        self.industry_letter    = industry_letter
        self.industry_name      = industry_name
        return
    
    def __repr__(self):
        return f'ESTABLISHMENT: \n\tUID: {self.uid}, \n\tEMPLOYEE SIZE: {self.employee_size} \n\tEMPLOYEES: {type(self.employees)} \n\tINDUSTRY: {self.industry_letter} \n\t\t{self.industry_name}'