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

function uploadProjectsNames() {
    jsonData.projectsNames.forEach(name => {
        let option = document.createElement('option')
        option.innerText = name
        option.setAttribute('value', name)
        dropdownProjects.appendChild(option)
    })
}
// function uploadSamplesNames(projectName) {
//     jsonData.samplesNames.forEach(name => {
//         let option = document.createElement('option')
//         option.innerText = name
//         option.setAttribute('value', name)
//         dropdownSamples.appendChild(option)
//     })
// }
function uploadNames(names, dropdown) {
    names.forEach(name => {
        let option = document.createElement('option')
        option.innerText = name
        option.setAttribute('value', name)
        dropdown.appendChild(option)
    })
}

// uploadProjectsNames()
uploadNames(jsonData.projectsNames, dropdownProjects)

dropdownProjects.addEventListener('click', e => {
    if (!e.target.value) return
    let projectName = e.target.value
    uploadNames(jsonData.samplesNames, dropdownSamples)
})