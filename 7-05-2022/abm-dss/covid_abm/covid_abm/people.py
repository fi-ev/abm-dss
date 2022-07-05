import numpy as np
import defaults as df
#from . import defaults

class People():
    def __init__(self, uid, age, sex, contacts):
        self.uid = uid
        self.age = age
        self.sex = sex
        
        #states
        self.susceptible = np.full(len(self.uid), True, dtype = bool)           #susceptible
        self.exposed     = np.full(len(self.uid), False, dtype = bool)          #exposed & with infected outcome
        self.exposed_f   = np.full(len(self.uid), False, dtype = bool)          #exposed but not infected
        self.infected    = np.full(len(self.uid), False, dtype = bool)          #infected

        self.variant     = np.full(len(self.uid), 0, dtype = np.int32)          #variant type
        
        #duration
        self.incubation  = np.full(len(self.uid), 0, dtype = np.int32)          #incubation duration
        self.inf_dur     = np.full(len(self.uid), 0, dtype = np.int32)          #duration infected
        
        
        self.contacts    = contacts
        
        return
    
    def init_infected(self, infected_count):
        """
        Randomly assign initial infected at the start of the simulation.

        Args:
            infected_count (int): initial infected agents count
        """
        
        #find susceptible indices
        sus_indices = np.where(self.susceptible == True)[0]
        
        #randomly infect a susceptible person
        inf_indices = df.rng.choice(sus_indices, infected_count, replace = False)
        
        #assign random variant?
        
        #change state from infected 
        self.infected[inf_indices] = True
        self.susceptible[inf_indices] = False
        
        return
    
    def find_infected_indices(self):
        
        indices = np.where(self.infected == True)[0]
        
        return indices
    
    def find_isolated_indices(self):
        
        return
    
    def subtract_nonzeros(self):
        return
        
    def update_susceptible_to_exposed(self):
        susc = np.where(self.susceptible == True)[0]
        self.susceptible[susc] = False
        self.exposed[susc]     = True
        return
    

    
    
    
    