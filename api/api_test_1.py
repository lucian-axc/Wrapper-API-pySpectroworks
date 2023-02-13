import api.pyspectroworks as pyspectroworks
import json

conn = pyspectroworks.connect('NGIyNzkxZjYtZmVmYy00NDRjLWFiYzUtZWIxYWI4ZjJiNzE4') # API key

def printClassAttributes(className):
    for attribute, value in className.__dict__.items():
        print(attribute, '=', value)

def printClassMethods(className):
    method_list = [method for method in dir(className) if method.startswith('__') is False]
    print(method_list)


# printClassAttributes(conn)
# printClassMethods(conn)


projects = conn.get_projects()
project = projects[9]
# printClassAttributes(project)
# printClassMethods(project)


items = project.get_items()
item = items[len(items) - 1]
# printClassAttributes(item)
# printClassMethods(item)



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

data = get_spectral_data(0, 400)
print('For wavelength: ', data[0], ' the attenuance is: ', data[1])