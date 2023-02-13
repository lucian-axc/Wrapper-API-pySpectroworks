import api.pyspectroworks as pyspectroworks
import json

import sys
sys.stdout.reconfigure(encoding='utf-8') #so that characters like greek mu can be accepted (fx in project names without causing a crash)


conn = pyspectroworks.connect('NGIyNzkxZjYtZmVmYy00NDRjLWFiYzUtZWIxYWI4ZjJiNzE4') # API key

def printClassAttributes(className):
    for attribute, value in className.__dict__.items():
        print(attribute, '=', value)

def printClassMethods(className):
    method_list = [method for method in dir(className) if method.startswith('__') is False]
    print(method_list)


# printClassAttributes(conn)
# printClassMethods(conn)
# print(dir(conn))

projects = conn.get_projects()
project = projects[9]
items = project.get_items()
item = items[len(items) - 1]

# printClassAttributes(project)
# printClassMethods(project)
# printClassAttributes(item)
# printClassMethods(item)


# print(dir(project))
# value = project.results
# print("Attribute: ", value)

# d = {
#     "data": value
# }
# json_object = json.dumps(d, indent = 2)
# print(json_object)


# print(dir(item))
# # print(item.)
# value = item.size_distribution
# print("Attribute: ", value)

# d = {
#     "data": value
# }
# json_object = json.dumps(d, indent = 2)
# print(json_object)

def extract_spectra(item):
    spectra = {
        "reference_B": item.get_spectrum("reference_B"),
        "sample_A": item.get_spectrum("sample_A"),
        "sample_B": item.get_spectrum("sample_B"),
        "sample_D": item.get_spectrum("sample_D")
    }
    # 'reference_B' (B side reference spectrum)
    # 'sample_A'    (A side sample spectrum)
    # 'sample_B'    (B side sample spectrum)
    # 'sample_D'    (D side sample spectrum)

    # print(spectra)
    return spectra

def parse_items(project):
    parsed_items = []
    for it in project.get_items():
        it_dict = {
            "_file_id": it._file_id,
            "_project_id": it._project_id,
            "box_code": it.box_code,
            "completeness": it.completeness,
            "created": it.created,
            "cuvette_idx": it.cuvette_idx,
            "get_size_distribution": it.get_size_distribution(),
            "spectra": extract_spectra(it),
            "hidden": it.hidden,
            "modified": it.modified,
            "results": it.results,
            "sample_attributes": it.sample_attributes,
            "size_distribution": it.size_distribution
        }
        # print(it_dict)
        parsed_items.append(it_dict)
    return parsed_items

def parse_all_projects():
    all_projects_parsed = []
    for pj in projects:   
        pj_dict = {
            "_project_id": pj._project_id,
            "created": pj.created,
            "items": parse_items(pj),
            "modified": pj.modified,
            "num_files": pj.num_files,
            "project_name": pj.project_name,
            "results": pj.results
        }
        all_projects_parsed.append(pj_dict)
    return all_projects_parsed

container = {
    "projects": parse_all_projects()
}

json_object = json.dumps(container, indent = 2)
print(json_object)










# print(item.results['refractive_index']['value'])

spectra_list = [ 'reference_B', 'sample_A', 'sample_B', 'sample_D' ]
# 'reference_B' (B side reference spectrum)
# 'sample_A'    (A side sample spectrum)
# 'sample_B'    (B side sample spectrum)
# 'sample_D'    (D side sample spectrum)

def get_spectral_data(spectrum_x, wavelength_target):
    spectrum = item.get_spectrum(spectra_list[spectrum_x])
    
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
        return 'Wavelength out of interval!'

# data = get_spectral_data(0, 400)
# print('For wavelength: ', data[0], ' the attenuance is: ', data[1])



