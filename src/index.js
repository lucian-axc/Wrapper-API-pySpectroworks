// class ProjectSampleSpectra {
//     constructor(projectName) {
//         this.projectName = projectName
//         this.sampleName = ''
//         this.spectrum = {}
//     }
// }

// # 'reference_B' (B side reference spectrum)
// # 'sample_A'    (A side sample spectrum)
// # 'sample_B'    (B side sample spectrum)
// # 'sample_D'    (D side sample spectrum)

let dropdownProjects = document.getElementById('projects-names')
let dropdownSamples = document.getElementById('samples-names')
let containerAllSpectra = document.getElementById('container-all-spectra')

let projectsNames = jsonData.projectsWithSamples.map(entry => entry.projectName)
let projectName = ''   //to be added in class definition
let samplesNames = []  //to be added in class definition
let sampleName = ''    //to be added in class definition

//helper functions
function uploadNames(names, dropdown) {
    for (let i in names) {
        let option = document.createElement('option')
        option.innerText = names[i]
        option.setAttribute('value', i)
        dropdown.appendChild(option)
    }
}

function renderSpectraContainers() {
    let containerAllSpectra = document.getElementById('container-all-spectra')
    
    types = [
        ['reference_B', 'B side reference'],
        ['sample_A', 'A side sample'],
        ['sample_B', 'B side sample'],
        ['sample_D', 'D side sample']
    ]
    types.forEach(type => {
        containerAllSpectra.innerHTML += `
            <div class="container-spectrum">
                <h3>${type[1]} spectrum</h3>
                <div class="container-w-a-data">
                    <div class="target-w-bar">
                        <p>Target wavelength:</p>
                        <input class="input-w" type="text" placeholder="type wavelength...">
                        <button class="btn-get-data" value="${type[0]}">Go!</button>
                    </div>
                    <div class="w-a-result">
                        <p>Wavelength:</p>
                        <p class="data-result wavelength-${type[0]}">see value...</p>
                    </div>
                    <div class="w-a-result">
                        <p>Attenuance:</p>
                        <p class="data-result attenuance-${type[0]}">see value...</p>
                    </div>
                </div>
            </div>
        `
    })
}

function getSpectrumPair(spectrumType, targetWavelength) {
    let pair = jsonData.spectra[spectrumType]
    let wavelength = '', attenuance = ''
    
    if (Array.isArray(pair)) {
        wavelength = pair[0]
        attenuance = pair[1]
    }

    return { wavelength, attenuance }
}

function renderSpectrumPair(spectrumType, pair) {
    document.querySelector(`.wavelength-${spectrumType}`).innerText = pair.wavelength || 'Not available'
    document.querySelector(`.attenuance-${spectrumType}`).innerText = pair.attenuance || 'Not available'
}

// Event Listeners
dropdownProjects.addEventListener('click', e => {
    dropdownSamples.innerHTML = '<option value="" default>- - -</option>'  
    if (!e.target.value) return

    let pjIndex = e.target.value

    projectName = jsonData.projectsWithSamples[pjIndex].projectName
    samplesNames = jsonData.projectsWithSamples[pjIndex].samplesNames

    uploadNames(samplesNames, dropdownSamples)
})

dropdownSamples.addEventListener('click', e => {
    let i = e.target.value
    sampleName = samplesNames[i]
    console.log('Sample index is: ', i)
})

containerAllSpectra.addEventListener('click', ({ target }) => {
    let { type, value } = target
    let wavelengthTarget = Number(target.previousElementSibling.value)
    
    if (type != 'submit' || !wavelengthTarget) return

    let spectrumType = value    
    let pair = getSpectrumPair(spectrumType, wavelengthTarget)
    renderSpectrumPair(spectrumType, pair)
})

uploadNames(projectsNames, dropdownProjects)
renderSpectraContainers()

