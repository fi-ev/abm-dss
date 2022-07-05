import numpy as np
import defaults as df

from . import data

def initialize_schools(parameters, barangay_init):
    
    print(f'Initializing schools . . .')
    schools  = data.load_schools(parameters['location'])
    colleges = data.load_colleges(parameters['location'])
    
    schools_init = {}
    
    for i,key in enumerate(schools.keys()):
        schools_init[key] = schools[key]
        
    for i,key in enumerate(colleges.keys()):
        schools_init[key].extend(colleges[key])
    
    n_schools = len(schools_init['names'])
    
    schools_init['uid']          = np.arange(n_schools, dtype=np.int32)
    schools_init['barangay_uid'] = map_brgy_name_to_brgy_uid(schools_init['barangay'], barangay_init)
    schools_init['grade_level']  = get_curriculum_grade_levels(schools_init['curriculum'])
    
    return schools_init

def map_brgy_name_to_brgy_uid(barangays, barangay_init):
   barangay_init_names = barangay_init['names']
   barangay_init_uid   = barangay_init['uid']
    
   dict_barangay_init = dict(zip(barangay_init_names, barangay_init_uid))
    
   uids = [dict_barangay_init[barangay] for i,barangay in enumerate(barangays)]
    
   return uids

def get_curriculum_grade_levels(curriculum):

   deped_grade_levels = data.deped_school_curriculum_grade_level_map
    
   grade_levels = {}
   for i,cur in enumerate(curriculum):
       grade_level_list = deped_grade_levels[cur]
       grade_levels[i] = grade_level_list
        
   return grade_levels

def count_grade_levels(grade_level):
    
    grade_level_counts = {}
    curriculum = data.school_curriculum_age_brackets
    
    for key in curriculum.keys():
        grade_level_counts[key] = 0
        
    for key in grade_level.keys():
        
        for level in grade_level[key]:
            grade_level_counts[level] += 1
    
    return grade_level_counts

def group_students_by_grade_level(students):
    students_ages = students['ages']
    students_uid  = students['uid']
    
    curriculum = data.school_curriculum_age_brackets
    
    students_by_grade_level = {}
    for key in curriculum.keys():
        min_age, max_age = curriculum[key]
        students_indices = np.where(np.logical_and(students_ages >= min_age, students_ages <= max_age))[0]
        students_by_grade_level[key] = students_uid[students_indices]
        
        mask = np.ones(students_uid.size, dtype = bool)
        mask[students_indices] = False
        
        students_uid  = students_uid[mask]
        students_ages = students_ages[mask]

    return students_by_grade_level

def create_school_students_size(sch_init = None, students_by_grade_level = None, students = None):
    '''
        Create size for each schools' grade level. . .
    '''
    if students_by_grade_level == None:
        students_by_grade_level = group_students_by_grade_level(students)
    
    curriculum = data.school_curriculum_age_brackets
    
    grade_level_counts = count_grade_levels(sch_init['grade_level'])
    
    sizes = {}
    for key in curriculum.keys():
        size = int(len(students_by_grade_level[key]) / grade_level_counts[key])
    
        all_sizes = df.rng.normal(size, 1, grade_level_counts[key])
        sizes[key] = list(map(int, all_sizes))

        sizes_sum = sum(sizes[key])
        if(sizes_sum < len(students_by_grade_level[key])):
            offset = len(students_by_grade_level[key]) - sizes_sum
            choose_indices = np.arange(len(sizes[key]))
            
            while(offset > 0):
                chosen_index = df.rng.choice(choose_indices)
                sizes[key][chosen_index] += 1
                offset-=1
                 
        elif(sum(sizes[key]) > len(students_by_grade_level[key])):
            offset = sizes_sum - len(students_by_grade_level[key]) 
            choose_indices = np.arange(len(sizes[key]))
            
            while(offset > 0):
                chosen_index = df.rng.choice(choose_indices)
                sizes[key][chosen_index] -= 1
                offset-=1
    
    
    return sizes


def assign_students(sch_init, students):
    '''
        Assign students to a school randomly. 
    '''
    
    students_by_grade_level = group_students_by_grade_level(students)
    
    sizes = create_school_students_size(sch_init, students_by_grade_level, students)
    
    schools = sch_init['grade_level']
    
    students = {}
    
    for key in schools.keys():
        school = schools[key]
        students[key] = {}
        for grade in school:
            students[key][grade] = []
            
            students_pool       = students_by_grade_level[grade]
            size                = sizes[grade].pop()
            students_assigned   = students_pool[:size]
            
            students[key][grade] = students_assigned
            
            indices = np.arange(len(students_assigned))
                    
            mask = np.ones(students_pool.size, dtype = bool)
            mask[indices] = False
            
            students_by_grade_level[grade] = students_by_grade_level[grade][mask]
                
    return students

def assign_students_nearest(sch_init, pop_households_assignment, students):
    '''
        Assign students to nearest school from their residence.
    '''

    
    
    return


def assign_school_employees(sch_init, employees):
    """

    Args:
        sch_init (dict): initialized school data
        employees (dict): chosen population that are employed 

    Returns:
        dict : 
        
    Notes:
        School employees refer to teachers and staff
    """
        
    schools_uid = sch_init['uid']
    employees_uid   = employees['uid']
    
    size = len(employees_uid) / len(schools_uid)

    sum_size = 0
    
    school_size = {}
    
    for uid in schools_uid:
        sizes               = df.rng.normal(size, 1.0, 1)
        school_size[uid]    = int(sizes[0])
        sum_size            += school_size[uid]

    if(sum_size < len(employees_uid)):
        offset          = len(employees_uid) - sum_size
        choice_schools  = np.arange(len(schools_uid))
        while(offset > 0):
            chosen_school = df.rng.choice(choice_schools, 1)
            school_size[chosen_school[0]] += 1
            offset-=1
            
    elif(sum_size > len(employees_uid)):
        offset          = sum_size - len(employees_uid)
        choice_schools  = np.arange(len(schools_uid))
        while(offset > 0):
            chosen_school = df.rng.choice(choice_schools, 1)
            school_size[chosen_school[0]] -= 1
            offset-=1
    
    employees_assignment = {}
    for uid in schools_uid:
        employees_assignment[uid] = []
        size = school_size[uid]
        
        employees_assigned        = employees_uid[:size]
        employees_assignment[uid] = employees_assigned 
        
        indices = np.arange(len(employees_assigned))
        
        mask            = np.ones(employees_uid.size, dtype = bool)
        mask[indices]   = False
        employees_uid   = employees_uid[mask]
        
    return employees_assignment


def create_schools(schools_init, assigned_students, assigned_teachers, assigned_school_staff):

    schools_grade_levels = schools_init['grade_level']
    

    schools = []

    for key in schools_grade_levels.keys():
        school = schools_grade_levels[key]
        
        classrooms      = []
        all_students    = []
        teachers        = []
        
        uid               = schools_init['uid'][key]
         

        for grade_level in school:
            
            g_level  = grade_level
            students = assigned_students[key][grade_level]
            
            classrooms.append(Classroom(grade_level = g_level, students = students))
            
            all_students.extend(students)
            
                
        name         = schools_init['names'][key]            
        barangay_uid = schools_init['barangay_uid'][key]
        g_levels     = schools_init['grade_level'][key]     
        staff        = assigned_school_staff[key]
        teachers     = assigned_teachers[key]
        
        schools.append(School(uid           = uid, 
                              name          = name, 
                              barangay_uid  = barangay_uid, 
                              grade_levels  = g_levels, 
                              classrooms    = classrooms,
                              all_students  = all_students,
                              teachers      = teachers,
                              staff         = staff))

        
    return schools

def create_schools_dict(schools_init, assigned_students, assigned_teachers, assigned_school_staff):
    
    schools_grade_levels = schools_init['grade_level']
    
    schools_dict = {}
    schools_dict['uid']             = []
    schools_dict['names']            = []
    schools_dict['barangay_uid']    = []
    schools_dict['grade_levels']     = []
    schools_dict['teachers']        = []
    schools_dict['staff']           = []
    schools_dict['classrooms']      = {}
    
    for key in schools_grade_levels.keys():
        school            = schools_grade_levels[key]
        uid               = schools_init['uid'][key]
        str_id            = str(uid)
         
        schools_dict['classrooms'][str_id] = {}
        
        for grade_level in school:
            g_level  = grade_level
            students = assigned_students[key][grade_level]
            
            schools_dict['classrooms'][str_id][g_level] = []
            schools_dict['classrooms'][str_id][g_level].extend(students)
            
        name         = schools_init['names'][key]            
        barangay_uid = schools_init['barangay_uid'][key]
        g_levels     = schools_init['grade_level'][key]     
        staff        = assigned_school_staff[key]
        teachers     = assigned_teachers[key]
        
        schools_dict['uid'].append(uid)
        schools_dict['names'].append(name)
        schools_dict['barangay_uid'].append(barangay_uid)
        schools_dict['grade_levels'].append(school)
        schools_dict['teachers'].append(teachers)
        schools_dict['staff'].append(staff)
        
    return schools_dict

def get_available_keys():
    keys = ['uid', 'names', 'barangay_uid', 'grade_level', 'teachers', 'staff', 'classrooms']
    return keys

class School():
    def __init__(self, uid, name, barangay_uid, grade_levels, teachers, staff, all_students, classrooms):
        self.uid             = uid
        self.name            = name
        self.barangay_uid    = barangay_uid
        self.grade_levels    = grade_levels
        self.teachers        = teachers
        self.staff           = staff
        self.all_students    = all_students
        self.classrooms      = classrooms
        return
    
    def __repr__(self):
        return f'SCHOOL {self.uid}:     \
                \n\tNAME: {self.name}   \
                \n\tBARANGAY_UID: {self.barangay_uid} \
                \n\tGRADE LEVELS: {self.grade_levels} \
                \n\tCLASSROOMS: {self.classrooms}     \
                \n\tTEACHERS: {self.teachers}         \
                \n\tSCHOOL STAFF: {self.staff} ' 

class Classroom():
    def __init__(self, grade_level, students):
        self.grade_level = grade_level
        self.students    = students
    
