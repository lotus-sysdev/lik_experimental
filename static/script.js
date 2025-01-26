document.addEventListener('DOMContentLoaded', function () {
    const editForm = document.getElementById('editForm');

    if (editForm) {
        editForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Fetch data from the form
            const formData = new FormData(editForm);

            // Make an asynchronous POST request
            fetch(editForm.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                // Clear existing error messages
                clearFormErrors();

                if (data.success) {
                    // Show alert for success
                    alert('Details updated successfully!');
                    // Get the customizable redirect URL from the form
                    const redirectUrl = editForm.dataset.redirecturl;
                    if (redirectUrl) {
                        // Redirect to the customizable URL
                        window.location.href = redirectUrl;
                    }
                } else {
                    // Update the page to display the errors
                    updateFormErrors(data.errors);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    function updateFormErrors(errors) {
        // Display new error messages
        for (const field in errors) {
            const errorMessages = errors[field];
            const fieldElement = document.querySelector(`[name="${field}"]`);
            
            if (fieldElement) {
                const errorContainer = document.createElement('div');
                errorContainer.className = 'error';
                errorContainer.innerText = errorMessages.join(', ');
                fieldElement.parentNode.appendChild(errorContainer);
            }
        }
    }

    function clearFormErrors() {
        const errorElements = document.querySelectorAll('.error');
        errorElements.forEach(element => element.remove());
    }
});

function confirmDelete(redirect) {
    if (confirm('Are you sure you want to delete?')) {
        $.ajax({
            type: 'POST',
            url: $('#deleteForm').attr('action'),
            data: $('#deleteForm').serialize(),
            success: function () {
                alert('Delete successful!');
                // You can optionally update the page or perform additional actions here
                // Navigate back to the customer list
                window.location.href = redirect;
            },
            error: function () {
                alert('Error deleting.');
            }
        });
    }
    return false;
}
