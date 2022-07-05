
from contextlib import AbstractAsyncContextManager
from . import barangay              as brgy
from . import schools               as sch
from . import households            as hh
from . import establishments        as est
from . import hcfacilities          as hcf
from . import pop 
from . import contact_networks      as cnx

import sys
import json
import gzip
import numpy as np
import defaults as df

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        
        elif isinstance(obj, np.floating):
            return float(obj)
        
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        
        return json.JSONEncoder.default(self, obj)
    
class Main():
    def __init__(self, parameters = None):
        
        #set default parameters first
        self.params = df.covid_params
        print(f'Default parameters: {self.params}')
        
        #set user parameters
        if parameters != None:
            self.update_parameters(parameters)
   
        #set seed
        self.set_seed()
        
        return
    
    def update_parameters(self, parameters):
        """
        
        Update parameters using user defined parameters.

        Args:
            parameters (dict): dictionary of parameter data
        
        TODO: parameter key validation
        
        """
        
        self.params = parameters
        
        print(f'User parameters: {self.params}') 
        
        return
    
    def set_seed(self):
        """
        
        Set default numpy rng.
        
        """
        
        #get seed parameter
        seed = int(self.params['seed'])
        
        #random seed if seed is 0
        if(seed == 0):
            df.rng = np.random.default_rng()
        #set seed if seed is not 0
        else:
            df.rng = np.random.default_rng(seed) 


    def create_synthpop_data(self, to_gzip = True):
        """
        Creation of synthpop data.

        Args:
            to_gzip (bool, optional): Store data as to gzip. Defaults to True.
        Returns:
            dict                    : dictionary of synthpop data.
            
        """
        try:
            loc_data = self.initialize_loc()
            pop_data = self.initialize_pop(loc_data)
        except:
            sys.exit(f'Could not acquire data')

        self.synthpop = {}
        self.synthpop['barangays']      = brgy.create_barangays_dict(loc_data['barangays'], loc_data['households'], loc_data['schools'])
        self.synthpop['households']     = hh.create_households_dict(loc_data['households'], pop_data['households'])
        self.synthpop['schools']        = sch.create_schools_dict(loc_data['schools'], pop_data['schools']['students'], pop_data['schools']['teachers'], pop_data['schools']['staff'])
        self.synthpop['hcfacilities']   = hcf.create_hcfacilities_dict(loc_data['hcfacilities'])
        self.synthpop['establishments'] = est.create_establishments_dict(loc_data['establishments'], pop_data['establishments'])
            
        self.synthpop['population']     = pop_data['population']

        if to_gzip:
            self.write_to_gzip('synthpop', self.synthpop)

        return self.synthpop
       
        
    def initialize_loc(self):
        
        """
        Initialize all location from data and store to dictionary. Not called directly.
            
        Returns:
            loc_data (dict) : dictionary of initialized location data
        """
        brgy_init   = brgy.initialize_barangay(self.params)                     #initialize barangay from data
        hh_init     = hh.initialize_households(self.params, brgy_init)          #initialize households from data
        sch_init    = sch.initialize_schools(self.params, brgy_init)            #initialize schools from data
        hcf_init    = hcf.initialize_hcfacility(self.params, brgy_init)         #initialize healthcare facilities from data
        est_init    = est.initialize_establishments(self.params)                #initialize establishments from data
        
        #pop_init    = pop.initialize_population(self.params, brgy_init)
        
        loc_data = {}
        avail_locs = self.return_all_avail_locs()
        
        for locs in avail_locs:
           loc_data[locs] = {}
        
        loc_data['barangays']        = brgy_init
        loc_data['households']       = hh_init
        loc_data['schools']          = sch_init
        loc_data['hcfacilities']     = hcf_init
        loc_data['establishments']   = est_init 
        
        return loc_data
    
    def initialize_pop(self, loc_data = None):
        
        """
        
        Initialize the population: Assign to households, assign students, assign employed, assign employed to workplaces.

        Args:
            loc_data (dict) : dictionary of initialized location data.
            
        Returns:
            pop_data (dict) : dictionary of population assignment
                
        """
        #if population is not created based on household data then use this function call
        pop_init = pop.initialize_population(self.params, loc_data['barangays'])
        #else:
        
        #labor_force = np.where(pop_init['ages'] >= 15)[0]
        population_count = pop_init['uid']
        
        print(f'Total Population: {len(population_count)}')
        
        pop_to_assign = pop_init
        
        students, pop_to_assign      = pop.get_students(self.params, pop_to_assign)                                                    #assign portion of population as students
        employed_left, unemployed    = pop.get_employed(self.params, pop_to_assign)                                #assign portion of population as employed
        
        teachers     , employed_left                = pop.get_teachers(self.params, employed_left)                                #assign a portion of employed as teachers
        staff        , employed_left                = pop.get_school_staff(self.params, employed_left)                            #assign a portion of employed as school staff
        establishment_employees , employed_left     = pop.get_establishment_employees(loc_data['establishments'], employed_left)  #assign a portion of employed as establishment employees
        
        pop_data = {}
        avail_locs = self.return_all_avail_locs()
        
        for locs in avail_locs:
           pop_data[locs] = {}
        
        #assign the population to specific location based on profession
        assigned_students                           = sch.assign_students(loc_data['schools'], students)
        assigned_teachers                           = sch.assign_school_employees(loc_data['schools'], teachers)
        assigned_school_staff                       = sch.assign_school_employees(loc_data['schools'], staff)
        assigned_establishment_employees            = est.assign_employees(loc_data['establishments'], establishment_employees)
        pop_households_assignment                   = hh.assign_household_members(self.params, loc_data['households'], pop_init)
        
        pop_data['population']                 = pop_init
        pop_data['households']                 = pop_households_assignment
        pop_data['schools'] = {}
        pop_data['schools']['students']        = assigned_students
        pop_data['schools']['teachers']        = assigned_teachers
        pop_data['schools']['staff']           = assigned_school_staff
        pop_data['establishments']             = assigned_establishment_employees
        
        return pop_data
    
    
    def return_all_avail_locs(self):
        
        all_loc = ['barangays', 'households', 'establishments', 'hcfacilities', 'schools']
        
        return all_loc
    
    def create_population(self, pop_init, households, schools, establishments):
    
        contacts = cnx.create_contact_networks(pop_init, households, schools, establishments)

        population = pop.create_population(pop_init, households, schools, establishments, contacts)
        
        return population
    
    def write_to_json(self, filename = '', data = None):
        
        #path = os.getcwd()
        #filepath = os.path.abspath(os.path.join(path, os.pardir)) + '/results/' + filename + '.json'
        
        #temporary path for now, to prevent ajax refresh ugh
        filepath = 'C:/Users/pagiy/Documents/NICER/DSS/results/' + filename + '.json' 
        
        
        with open(filepath, 'w') as json_file:
            try:
                json.dump(data, json_file, ensure_ascii = False, cls = NumpyEncoder)
            except:
                print('cannot access json')
                sys.exit()
                
    def write_to_gzip(self, filename = '', data = None):
        """
        Write data to gzip format.

        Args: 
            filename (str) : name of the file to save.
            data     (dict): dictionary of the data to save to file

        """
        
        filepath = 'C:/Users/pagiy/Documents/NICER/DSS/results/' + filename
        
        with gzip.open(filepath, 'wt', encoding="ascii") as zipfile:
            json.dump(data, zipfile, cls = NumpyEncoder)

        print(f'Succesfully saved as gzip file with filename: {filename}.')
    
    def read_gzip(self, filename = ''):
        
        """
        Read gzip data.

        Args: 
            filename (str) : name of the file to read.
            data     (dict): dictionary of the data to save to file

        """   
        
        filepath = 'C:/Users/pagiy/Documents/NICER/DSS/results/' + filename
        
        with gzip.open(filepath, 'rt', encoding="ascii") as zipfile:
            data = json.load(zipfile)
        
        return data
                     
        
        
