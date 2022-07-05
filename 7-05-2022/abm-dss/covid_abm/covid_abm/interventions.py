class Interventions():
    def __init__(self, name = ''):
        self.name = name
        return

class Testing(Interventions):
    def __init__(self):
        super().__init__('Testing')
        return
    
class Isolate(Interventions):
    def __init__(self):
        super().__init__('Isolate')
        return
    
    #find infected indices with conditions: 1. days since symptoms show; 2. infectious == True
    
    #if days since symptoms show >= 3
        #days counter = 5
    #else 

    #add days counter 
    
    #toggle isolating to true
    
      
class Quarantine(Interventions):
    def __init__(self):
        super().__init__('Quarantine')
        return
    
    #find exposed and exposed_inf indices 
    
    #toggle quarantine to true
    
    #add days counter
    
class Vaccination(Interventions):
    def __init__(self):
        super().__init__('Vaccination')   
    
    #randomly choose susceptible 
    
    #