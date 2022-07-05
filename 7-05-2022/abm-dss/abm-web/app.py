from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

try:
    import synthpop as sp
except:
    print(f'synthpop module not found')

try:
    import covid_abm as cvabm
except:
    print(f'covid_abm module not found')
    
import numpy as np
import json, gzip, sys


app = Flask(__name__)

cors = CORS(app, resources = {r"/abm/*": {"origins": "*"}})


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
  
def read_json(filename = ''):
    
    '''
        read json file
    '''
    #path = os.getcwd()
    #filepath = os.path.abspath(os.path.join(path, os.pardir, 'results', filename + '.json' ))
    
            
    #temporary path for now, to prevent ajax refresh ugh
    filepath = 'C:/Users/pagiy/Documents/NICER/DSS/results/' + filename + '.json' 
        
    with open(filepath, 'r') as json_file:
        try:
            data = json.load(json_file)
        except:
            print('cannot access json')
            sys.exit()
            
    return data

def read_gzip(filename = ''):
    
    #temporary path for now, to prevent ajax refresh ugh
    filepath = 'C:/Users/pagiy/Documents/NICER/DSS/results/' + filename
        
    with gzip.open(filepath, 'rt', encoding="ascii") as zipfile:
        data = json.load(zipfile)
        
    return data
            
@app.route('/abmbe/get/<region>')
def get_region(region):
    
    '''
        return json details of a region
    '''
    
    with open('./static/regions.json', 'r') as file:
        data = json.load(file)
        
    region = region.lower()
    
    return data[region]


@app.route('/abmbe/post/initialize_synthpop', methods = ['POST'])
def initialize_synthpop():
    
    '''
        initialize synthetic population
    '''
    
    user_params = request.get_json(force = True)
    
    parameters = {}
    for key in user_params.keys():
        parameters[key] = user_params[key]
    
    sp_main = sp.Main(parameters['parameter_proxy'])
    
    try:

        sp_main.create_synthpop_data(to_gzip = True)
        
        return f'success'
    except:
        return f'failed'

@app.route('/abmbe/post/run_covid_abm', methods = ['POST'])
def run_covid_abm():
    
    user_params = request.get_json(force = True)
    
    parameters = {}
    for key in user_params.keys():
        parameters[key] = user_params[key]
    
    cv_abm = cvabm.Main(parameters['parameter_proxy'])
    
    try:
        cv_abm.run_simulation()
        return f'success'
    except:
        return f'failed'
    

#problem: json files are huge...
@app.route('/abmbe/get/synthpop/<filename>')
def get_synthpop_results(filename):
    
    '''
        entry point for getting synthpop results
    '''
    data = read_gzip('synthpop')
    if filename == 'barangays':
        data = data['barangays']

    return data


if __name__ == '__main__':
    app.run(debug = True)

