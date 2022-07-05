from . import contact_networks as cnx
from . import people
from . import rates

import defaults as df
import synthpop as sp
import numpy as np
import json, gzip, os


class Main():
    def __init__(self, parameters = None):
        
        self.params = df.covid_params           #set default parameters first
        
        if parameters != None:
            self.update_parameters(parameters)  #if parameters is supplied, update the current parameters

        self.set_seed()                         #set numpy seed
        
        return
    
    def update_parameters(self, parameters):
        
        print(f'Updating parameters:')
        
        self.params = parameters
        
        print(f'User parameters: {self.params}') 
        
        return
    
    def set_seed(self):
        
        seed = int(self.params['seed'])
        
        if(seed == 0):
            df.rng = np.random.default_rng()
            
        else:
            df.rng = np.random.default_rng(seed) 
        
        
    def get_data_from_synthpop(self, from_gzip = True):
        
        if from_gzip:
            data = self.read_gzip('synthpop')
        else:
            print(f'create synthpop')
            sp_main = sp.Main(self.params)
            sp_main.initialize_pop()
        
        return data
    
    def make_pop_from_synthpop(self):
        """
        Make a population dictionary 

        Returns:
            dict: population dictionary of all population properties generated from synthetic population
        """
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
        
        print(pop.keys())
        return pop

    def create_people(self):
        
        #properly create a population dictionary generated from synthetic population
        pop = self.make_pop_from_synthpop()
        self.ppl = people.People(pop['uid'], pop['ages'], pop['sexes'], pop['contacts'])
        
        #initialize infected 
        self.ppl.init_infected(self.params['infectious_count'])
        
        print(f'Done population')
        
        return 
    
    def initialize_interventions():
        
        return
    
    def run_simulation(self):
        
        self.create_people()
        
        print(f'SIMULATION RUN: ')
        
        end_day = int(self.params['days'])
        
        t = 0
        
        # #main loop here
        while(t < end_day):
            
            #for every intervention, apply intervention 
            
            #update states (days) 
            
            #find infected and not isolated indices for contact computation
            inf_inds = self.ppl.find_infected_indices()
            
            for ind in inf_inds:
                
                for key, layer in self.ppl.contacts[ind].items():
                    p1 = ind
                    p2 = layer
                    
                    #find susceptible contacts
                    inds = np.where(self.ppl.susceptible[p2] == True)[0]
                    
                    #randomly infect using simple random sampling
                    res = np.random.choice([True, False], len(inds))
                    new_inf = res[res == True]
                    
                    
                
            #get results
            
            t+=1
        #     #check/update states
            
        #     #find infected and not isolated indices for contact computation
        #     inds = self.ppl.find_infected_indices()     

        #     #loop through each infected
        #     for ind in inds:
                
        #         #loop through contacts of infected. key == contact layer, layer == the contacts within that layer
        #         for key, layer in self.ppl.contacts[ind].items():
        #             p1 = ind
        #             p2 = layer
                    
        #             #calculate transmission from infected to susceptible
        #             res = rates.compute_transmission_rates(p1,p2)
                    
        #             #calculate susceptibles 
        #             print(p1)
        #             print(p2)
        #             print(res)
        #             #compute contacts
        #             #rates.compute_transmission_rates()
            
        #     #increase day by 1
        #     T += 1
        
        return
    
    def compute_contacts(self, indices):
        
        
        return
    
    def read_gzip(self, filename = '', filepath = ''):
        
        filepath = 'C:/Users/pagiy/Documents/NICER/DSS/results/' + filename
        
        if os.path.exists(filepath):
            with gzip.open(filepath, 'rt', encoding="ascii") as zipfile:
                data = json.load(zipfile)
        else:
            raise FileNotFoundError(f'No available synthpop data. Try initializing synthpop first.')
        
        return data
    
    
    
class Results():
    def __init__(self):
        return
    
    
    
    
    