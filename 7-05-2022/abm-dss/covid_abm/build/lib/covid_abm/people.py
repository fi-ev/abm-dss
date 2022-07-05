import numpy as np
from . import defaults

class People():
    def __init__(self, uid, age, sex):
        self.uid = uid
        self.age = age
        self.sex = sex
        
        #states
        self.susceptible = np.full(len(self.uid), True, dtype = bool)
        self.exposed     = np.full(len(self.uid), False, dtype = bool)
        self.infected    = np.full(len(self.uid), False, dtype = bool)
        
        #duration
        self.incubation  = np.full(len(self.uid), 0, dtype = np.int32)
        self.inf_dur     = np.full(len(self.uid), 0, dtype = np.int32)
        
        return
    
    def init_infected(self, infected_count):
        '''
            randomly assign initial infected at the start of the simulation.
        '''
        print(infected_count)
        
        sus_indices = np.where(self.susceptible == True)[0]
        
        inf_indices = defaults.rng.choice(sus_indices, infected_count, replace = False)
        
        self.infected[inf_indices] = True
        self.susceptible[inf_indices] = True
        
        #test print
        test = np.where(self.infected == True)[0]
        
        return
    
    def update_durations(self):
        
        return
    
    
    def update_susceptible_to_exposed(self):
        susc = np.where(self.susceptible == True)[0]
        self.susceptible[susc] = False
        self.exposed[susc]     = True
        return
    
    def to_infectious(self):
        
        return
    
    def to_infected(self, indices):

        return
    
    
    
    