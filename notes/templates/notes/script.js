function analyzeImage() {
    const inputElement = document.getElementById('uploadImage');
    const file = inputElement.files[0];

    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    fetch('/api/analyze/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error('Error:', error));
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    const colors = data.colors;
    for (let i = 0; i < colors.length; i++) {
        const colorDiv = document.createElement('div');
        colorDiv.style.backgroundColor = `rgb(${colors[i][0]}, ${colors[i][1]}, ${colors[i][2]})`;
        colorDiv.style.width = '50px';
        colorDiv.style.height = '50px';
        colorDiv.style.display = 'inline-block';
        colorDiv.style.margin = '5px';
        resultsDiv.appendChild(colorDiv);
    }
}
