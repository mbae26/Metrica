document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData(this);
    var messageElement = document.getElementById('message');
    var submitButton = this.querySelector('[type="submit"]');
    
    // Disable the submit button to prevent multiple submissions and display a loading message
    submitButton.disabled = true;
    messageElement.innerHTML = 'Uploading and processing...';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            // If the server response is not ok, throw an error
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.text();
    })
    .then(data => {
        messageElement.innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
        messageElement.innerHTML = 'An error occurred while submitting the model.';
    })
    .finally(() => {
        // Re-enable the submit button after the fetch is complete
        submitButton.disabled = false;
    });
});
