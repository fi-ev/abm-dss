import networkx as nx
import numpy as np

from . import defaults

def create_contact_networks(population,
                            barangays,
                            households,
                            establishments,
                            schools
                            ):
    '''
        NOTE: Uses dictionary data to create contacts
    '''
    
    contacts = {}

    contacts['households']                              = create_households_contacts(households)
    contacts['community']                               = create_community_contacts(barangays, households)
    contacts['establishments']                          = create_establishments_contacts(establishments)
    contacts['schools'], contacts['classrooms']         = create_schools_contacts(schools)
    
    pop_uid = population['uid']
    
    print(f'Finalizing Contacts... ')
    pop_contacts = {}
    
    for id in pop_uid:
        pop_contacts[id] = {}
        for key in contacts.keys():
            if id in contacts[key]:
                pop_contacts[id][key] = contacts[key][id]
            else:
                pop_contacts[id][key] = []
    
    return pop_contacts


def create_households_contacts(households):
    
    print(f'Creating Households Contacts')
    
    contacts = {}
    
    for i,member in enumerate(households['members']):
        nodes = member
        contacts.update(random_graph(nodes, 1.0))
    
    print(f'Done Households Contacts')
    
    return contacts

def create_community_contacts(barangays, households, random = True):
    
    contacts = {}
    if random:
        for i,household in enumerate(barangays['households']):
            nodes = [members for hh in household for members in households['members'][hh]]
            contacts.update(random_graph(nodes, 10))    
        
    return contacts

def create_establishments_contacts(establishments):
    
    print(f'Creating Establishments Contacts')
    
    contacts = {}
    
    p = 10
    for i,employees in enumerate(establishments['employees']):
        nodes = employees
        contacts.update(random_graph(nodes, p))

    print(f'Done Establishments Contacts')   
     
    return contacts


def create_schools_contacts(schools):
    
    print(f'Creating Schools Contacts')
    
    contacts = {}
    
    contacts['classrooms'] = {}
    contacts['schools']    = {}
    
    n_schools = len(schools['classrooms'].keys())
    
    for i in range(n_schools):
        
        school_teachers = schools['teachers'][i]
        school_staff    = schools['staff'][i]
        
        for key in schools['classrooms'][str(i)].keys():
            
            
            students = schools['classrooms'][str(i)][key]

            nodes = [students, school_teachers]
            #p = [ [students-students,  students->teachers],]
            #      [teachers->students, teachers-teachers ] ]    
            p     = [[0.5, 0.3],       #assumption
                    [0.3, 0.5]]
            
            contacts['classrooms'].update(stochastic_block_model(nodes, p))
        
        nodes = school_teachers + school_staff
        contacts['schools'].update(random_graph(nodes, 0.5))
        
    print(f'Done Schools Contacts')
    
    return contacts['schools'], contacts['classrooms']

def random_graph(nodes, p):
    
    n = len(nodes)
    
    if isinstance(p, float):
        prob = p
    else:
        prob = p / n
        
    if(prob >= 1.0):
        G = nx.complete_graph(n = n)
    else:
        G = nx.fast_gnp_random_graph(n = n, p = prob)
    
    dict_of_list = nx.to_dict_of_lists(G)
    
    contacts = {}
    
    for key in dict_of_list.keys():
        contacts[nodes[key]] = [nodes[d] for d in dict_of_list[key]]
        
    return contacts

def stochastic_block_model(nodes, p):
    
    all_nodes = []
    groups    = []
    for i in range(len(nodes)):
        groups.append(len(nodes[i]))
        all_nodes.extend(nodes[i])
    
    G = nx.stochastic_block_model(groups, p)
    
    dict_of_list = nx.to_dict_of_lists(G)
    
    contacts = {}
    

    for key in dict_of_list.keys():
        contacts[all_nodes[key]] = [all_nodes[d] for d in dict_of_list[key]]

    return contacts


