import pyspectroworks
import json
import sys

from util import client
from util import debugging

sys.stdout.reconfigure(encoding='utf-8') #so that characters like greek mu can be accepted (fx in project names without causing a crash)
api_key = client.client['api_key']

conn = pyspectroworks.connect(api_key)
projects = conn.get_projects()

#functions for data extraction
def get_names_projects_with_samples():
    projects_with_samples = []

    for pj in projects:
        pj_entry = {}
        samples_names = []
        samples = pj.get_items()
        
        if len(samples) > 0:
            for sample in samples:
                attr = sample.sample_attributes
                if attr.get('Sample name') != None:
                    samples_names.append(attr['Sample name'])
                else:
                    samples_names.append('<No sample name>') #sample item has no name, however it exists with all its data
        else:
            samples_names = None #project has no sample items

        pj_entry["projectName"] = pj.project_name
        pj_entry["samplesNames"] = samples_names
        projects_with_samples.append(pj_entry)
    
    return projects_with_samples

def get_projects_names():
    projects_names = []
    for pj in projects:
        projects_names.append(pj.project_name)
    return projects_names

def get_samples_and_names(project_name):
    i = projects_names.index(project_name)
    pj = projects[i]
    samples = pj.get_items()
    samples_names = []

    if len(samples) > 0:
        for sample in samples:
            attr = sample.sample_attributes
            if attr.get('Sample name') != None:
                samples_names.append(attr['Sample name'])
            else:
                samples_names.append('<No sample name>') #sample item has no name, however it exists with all its data
    else:
        return None #project has no sample items
    return [samples_names, samples]

def get_closest_wa_data(spectrum, wavelength_target):
    i = 0
    while i < len(spectrum):
        current_wave = spectrum[i][0]
        next_wave = spectrum[i + 1][0] #what about end of wavelength list? boundary problem
        current_att = spectrum[i][1]

        if round(current_wave, 3) == wavelength_target:
            return [current_wave, current_att]
        if current_wave <= wavelength_target and wavelength_target <= next_wave:
            if abs(wavelength_target - current_wave) < abs(wavelength_target - next_wave):
                return [current_wave, current_att]
            else:
                next_att = spectrum[i + 1][1]
                return [next_wave, next_att]
        
        i = i + 1
    
    if i == len(spectrum):
        return 'Target wavelength out of interval!'

def get_spectrum_wa_pair(project_name, sample_name, spectrum_type, wavelength_target):
    s_n = get_samples_and_names(project_name)
    samples_names = s_n[0]
    samples = s_n[1]

    i = samples_names.index(sample_name)
    spectrum = samples[i].get_spectrum(spectrum_type)
    
    return get_closest_wa_data(spectrum, wavelength_target)


projects_names = get_projects_names() #needed in get_samples_and_names
spectrum_types = [ 'reference_B', 'sample_A', 'sample_B', 'sample_D' ]
names_projects_with_samples = get_names_projects_with_samples()


pj_index = 6
s_index = 7
pj_name = names_projects_with_samples[pj_index]["projectName"]
s_name = names_projects_with_samples[pj_index]["samplesNames"][s_index]
spectrum_index = 2
wv_target = 700

def generate_arguments_and_pair(
        pj_index,
        s_index,
        spectrum_index,
        wv_target
    ):
    
            pj_name = names_projects_with_samples[pj_index]["projectName"]
            s_name = names_projects_with_samples[pj_index]["samplesNames"][s_index]

            return get_spectrum_wa_pair(
                pj_name,
                s_name,
                spectrum_types[spectrum_index],
                wv_target
            )

wa_pair_reference_B = generate_arguments_and_pair(9, 7, 0, 700)
wa_pair_sample_A = generate_arguments_and_pair(9, 7, 1, 339)
wa_pair_sample_B = generate_arguments_and_pair(9, 7, 2, 405)
wa_pair_sample_D = generate_arguments_and_pair(9, 7, 3, 220)


# Example
#  get_spectrum_wa_pair(
#     'Enzyme + VC + Water 27.05.2022',
#     'Water + VC + enzyme nr2',
#     'sample_A',
#     350
# )

container = {
    "projectsWithSamples": names_projects_with_samples,
    "spectra": {
        "reference_B": wa_pair_reference_B,
        "sample_A": wa_pair_sample_A,
        "sample_B": wa_pair_sample_B,
        "sample_D": wa_pair_sample_D
    }
}

json_object = json.dumps(container, indent = 2)
# print(json_object)

with open('../src/json_file.js', 'w') as file:
    file.write("let jsonData = ")
    
with open('../src/json_file.js', 'a') as file:
    file.write(json_object)


# 'reference_B' (B side reference spectrum)
# 'sample_A'    (A side sample spectrum)
# 'sample_B'    (B side sample spectrum)
# 'sample_D'    (D side sample spectrum)
