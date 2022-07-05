from . import contact_networks as cnx
from . import defaults
from . import people

import synthpop as sp
import numpy as np
import json, gzip

default_parameters = dict(
    location                = dict(
        region              = 'SOCCSKSARGEN',                          #should be from user data. which region they belong to. restricted to region       
        province            = 'South Cotabato',                        #user set. which province
        municipality        = 'General Santos'                         #user set. set municipality; setting municipality also gets data on province
    ),
                           
    seed                    = 0,                                       #set seed. 0 for random seed.
    infectious_count        = 1,                                       #population count that's infectious at the start
    days                    = 60,                                      #simulation time

    transmission_rates        = dict(
        households            = 0.5,                                    
        establishments        = 0.5,
        communities           = 0.5,
        schools               = 0.5,
        classrooms            = 0.5,          
    ),
    
    
)

class Main():
    def __init__(self, parameters = None):
        
        self.params = default_parameters
        
        print(f'Default parameters: {self.params}')
        
        if parameters != None:
            self.update_parameters(parameters)
   
        self.set_seed()
        
        return
    
    def update_parameters(self, parameters):
        
        print(f'Updating parameters:')
        
        self.params = parameters
        
        print(f'User parameters: {self.params}') 
        
        return
    
    def set_seed(self):
        
        seed = int(self.params['seed'])
        
        if(seed == 0):
            defaults.rng = np.random.default_rng()
            
        else:
            defaults.rng = np.random.default_rng(seed) 
        
        
    def get_data_from_synthpop(self, from_gzip = True):
        
        if from_gzip:
            data = self.read_gzip('synthpop')
        else:
            print(f'create synthpop')
            sp_main = sp.Main(self.params)
            sp_main.initialize_all(True)
        
        return data
    
    def make_pop_from_synthpop(self):
        
        print(f' Making population dictionary')
    
        data = self.get_data_from_synthpop(from_gzip = True)
            
        barangays       = data['barangays']
        population      = data['population']
        establishments  = data['establishments']
        hcfacilities    = data['hcfacilities']
        households      = data['households']
        schools         = data['schools']

        contacts        = cnx.create_contact_networks(population, barangays, households, establishments, schools)
        
        pop = {}
        
        n_pop = len(population['uid'])
        
        pop['uid']   = []
        pop['ages']  = []
        pop['sexes'] = []
        for i in range(n_pop):
            pop['uid'].append(population['uid'][i])
            pop['ages'].append(population['ages'][i])
            pop['sexes'].append(population['sexes'][i])
            
        households_id = np.empty(len(pop['uid']), dtype = np.int32)
        barangay_id   = np.empty(len(pop['uid']), dtype = np.int32)
        
        for i,uid in enumerate(households['uid']):
            households_id[households['members'][uid]] = households['uid'][uid]
            barangay_id[households['members'][uid]]   = households['barangay_uid'][uid]
            
            
        establishments_id = np.full(len(pop['uid']), -1, dtype = np.int32)
        
        for i,uid in enumerate(establishments['uid']):
            establishments_id[establishments['employees'][uid]] = establishments['uid'][uid]
                
        schools_id = np.full(len(pop['uid']), -1, dtype = np.int32)
        
        for i,uid in enumerate(schools['uid']):
            schools_id[schools['teachers'][uid]] = schools['uid'][uid]
            schools_id[schools['staff'][uid]]    = schools['uid'][uid]
            
            for key in schools['classrooms'][str(i)].keys():
                students = schools['classrooms'][str(i)][key]
                schools_id[students] = schools['uid'][uid]
        
        pop['barangay']         = barangay_id               #uid of barangay where this person lives
        pop['household']        = households_id             #uid of household where this person lives
        pop['school']           = schools_id                #uid of school where this person attends to
        pop['establishment']    = establishments_id         #uid of establishment where this person attends to
        pop['contacts']         = contacts
        
        
        print(f' Done making population dictionary')
        
        
        return pop

    def create_people(self):
        pop = self.make_pop_from_synthpop()
        self.ppl = people.People(pop['uid'], pop['ages'], pop['sexes'])
        self.ppl.init_infected(self.params['infectious_count'])
        
        return

    def step(self):
        
        return
    
    def run_simulation(self):
        
        self.create_people()
        
        T = 0
        
        while(T < self.params['days']):
            
            T += 1
        
        
        
        
        #main loop here
        
        return
    
    def read_gzip(self, filename = '', filepath = ''):
        
        filepath = 'C:/Users/pagiy/Documents/NICER/DSS/results/' + filename
        
        with gzip.open(filepath, 'rt', encoding="ascii") as zipfile:
            data = json.load(zipfile)
        
        return data
    
    
    