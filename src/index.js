// paragraph = document.getElementById('att')
// paragraph.textContent = jsonData['wavelength - attenuance']

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

let projectsNames = jsonData.projectsWithSamples.map(entry => entry.projectName)

function uploadNames(names, dropdown) {
    for (let i in names) {
        let option = document.createElement('option')
        option.innerText = names[i]
        option.setAttribute('value', i)
        dropdown.appendChild(option)
    }
}

uploadNames(projectsNames, dropdownProjects)

dropdownProjects.addEventListener('click', e => {
    dropdownSamples.innerHTML = '<option value="" default>- - -</option>'  
    if (!e.target.value) return

    let pjIndex = e.target.value
    let samplesNames = jsonData.projectsWithSamples[pjIndex].samplesNames
    uploadNames(samplesNames, dropdownSamples)
})