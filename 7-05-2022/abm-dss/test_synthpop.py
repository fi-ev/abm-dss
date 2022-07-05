import synthpop as sp
import defaults as df

loc = df.covid_params['location']
print(f'{loc}')

#====================================#
#========= Initializations ==========#
#====================================#


barangay_init = {}
households_init = {}
establishments_init = {}
hcfacilities_init = {}
schools_init = {}
pop_init = {}
employed_count = 0

def test_barangays_init():
    
    barangay_init.update(sp.brgy.initialize_barangay(df.covid_params))
    
    #print(barangay_init)
    
    return

def test_households_init():
    
    test_barangays_init()
    
    households_init.update(sp.hh.initialize_households(df.covid_params, barangay_init))
    
    print(households_init.keys())
    
    return

def test_schools_init():
    
    test_barangays_init()
    
    schools_init.update(sp.sch.initialize_schools(df.covid_params, barangay_init))
    
    #print(schools_init)
    
    return

def test_establishments_init():
    
    establishments_init.update(sp.est.initialize_establishments(df.covid_params))
    
    print(establishments_init)
    
    #return 

def test_hcfacilities_init():
    
    test_barangays_init()
    
    hcfacilities_init.update(sp.hcf.initialize_hcfacility(df.covid_params, barangay_init))
    
    #print(hcfacilities_init)
    
    return hcfacilities_init

#====================================#
#=========== POPULATION =============#
#====================================#

def test_pop_init():
    
    test_barangays_init()
    
    pop_init.update(sp.pop.initialize_population(df.covid_params, barangay_init))
    
    print(pop_init)
    
    return 

def test_students_assignment():
    
    test_pop_init()
    
    students, pop = sp.pop.get_students(df.covid_params, pop_init)
    
    n_students = len(students['uid'])
    
    #print(f' Number of students: {n_students}')
    
    return pop


def test_employed_assignment():
    
    pop_init = test_students_assignment()
    
    employed, unemployed = sp.pop.get_employed(df.covid_params, pop_init)
    
    n_employed = len(employed['uid'])
    
    #print(f' Number of employed {n_employed}')
    
    return employed


def test_teachers_assignment():
    
    employed = test_employed_assignment()
    
    teachers, employed_left = sp.pop.get_teachers(df.covid_params, employed)
    
    n_teachers = len(teachers['uid'])
    
    #print(f' Number of teachers: {n_teachers}')
    
    return employed_left


def test_staff_assignment():
    
    employed = test_teachers_assignment()
    
    staff, employed_left = sp.pop.get_school_staff(df.covid_params, employed)
    
    n_staff = len(staff['uid'])
    
    #print(f' Number of staff {n_staff}')
    
    return employed_left

def test_establishment_employees():
    
    test_establishments_init()
    
    employed = test_staff_assignment()
    
    establishment_employees, employed_left = sp.pop.get_establishment_employees(establishments_init, employed)
    
    n_est_employees = len(establishment_employees['uid'])
    
    #print(n_est_employees)
    
    return employed_left


def test_assign_students():
    
    test_schools_init()
    
    students = test_students_assignment()
    
    assigned_students = sp.sch.assign_students(schools_init, students)
    
    return assigned_students

def test_assign_teachers():
    
    test_schools_init()
    
    teachers = test_teachers_assignment()
    
    assigned_teachers = sp.sch.assign_school_employees(schools_init, teachers)

    print(assigned_teachers.keys())
    
    return assigned_teachers

def test_assign_staff():
    
    test_schools_init()
    
    staff = test_staff_assignment()
    
    assigned_staff = sp.sch.assign_school_employees(schools_init, staff)
    
    print(assigned_staff.keys())
    
    return assigned_staff

def test_assigned_establishment_emp():
    
    test_establishments_init()
    
    employees = test_establishment_employees()
    
    emp = sp.est.assign_employees(establishments_init, employees)
    
    print(emp.keys())
    
    return

    
#test_barangays_init() #ok
#test_households_init() #ok
#test_establishments_init() #ok
#test_hcfacilities_init() #ok
#test_schools_init() #ok

#test_pop_init() #ok

#test_students_assignment() #ok
#test_employed_assignment() #ok
#test_teachers_assignment() #ok
#test_staff_assignment() #ok
#test_establishment_employees() #ok

#test_assign_students() #ok
#test_assign_teachers() #ok
#test_assign_staff() #ok
#test_assigned_establishment_emp() #ok


#main = sp.Main(df.covid_params)
#main.create_synthpop_data(False)