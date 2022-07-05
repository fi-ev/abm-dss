'''
    Generate contacts for every location and assigned agent.

    NOTE: This uses list of classes to create contact networks. 

'''

import numpy as np
import networkx as nx

import defaults as df

def create_contact_networks(pop_init, households, schools, establishments):
    
    
    contacts = {}
    contacts['households']                          = create_households_contact(households)
    contacts['classrooms'], contacts['schools']     = create_schools_contacts(schools)
    contacts['establishments']                      = create_establishment_contacts(establishments)
    
    print(f'Finalizing contacts. . .')
    
    pop_uid = pop_init['uid']
    
    pop_contacts = {}
    for id in pop_uid:
        
        #need to convert to string for writing to json purposes
        str_id = str(id)
        pop_contacts[str_id] = {}
        for key in contacts.keys():
            if id in contacts[key]:
                pop_contacts[str_id][key] = contacts[key][id]
            else:
                pop_contacts[str_id][key] = []
                
    return pop_contacts


def create_households_contact(households):
    
    contacts = {}
    p = 1.0
    for i,hh in enumerate(households):
        nodes = hh.members
        contacts.update(random_graph(nodes, p))
    return contacts

def create_schools_contacts(schools):
    
    classrooms = {}     
    school     = {}
    
    for i,sch in enumerate(schools):
        classroom = sch.classrooms
        
        n_teachers = int(len(sch.teachers) / len(classroom))
        
        for room in classroom:
            
            teachers = df.rng.choice(sch.teachers, n_teachers, replace = False)
            #nodes = room.students
            nodes = [room.students, teachers]
            #p = [ [students-students,  students->teachers],]
            #      [teachers->students, teachers-teachers ] ]
            
            p      = [[0.4, 0.3],
                      [0.3, 0.5]]
            #classrooms.update(random_graph(nodes, p = 0.4))
            classrooms.update(stochastic_block_model(nodes, p))

        nodes = list(sch.teachers) + list(sch.staff)
        school.update(random_graph(nodes, p = 0.5))
        
    return classrooms, school

def create_establishment_contacts(establishments):
    contacts = {}
    
    p = 15
    
    for i,est in enumerate(establishments):
        nodes = est.employees
        contacts.update(random_graph(nodes, p))
        
    return contacts
    

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

