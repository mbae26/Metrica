document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData(this);
    var messageElement = document.getElementById('message');

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        messageElement.innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
        messageElement.innerHTML = 'An error occurred while submitting the model.';
    });
});
