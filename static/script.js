function update() {
    $.ajax({
        type: 'POST',
        url: $('#editForm').attr('action'),
        data: $('#editForm').serialize(),
        success: function () {
            alert('Update successful!');
            // You can optionally update the page or perform additional actions here
            // Example: $('#customerName').text($('#id_name').val());
        },
        error: function () {
            alert('Error updating details.');
        }
    });
}

function confirmDelete() {
    if (confirm('Are you sure you want to delete this customer?')) {
        $.ajax({
            type: 'POST',
            url: $('#deleteForm').attr('action'),
            data: $('#deleteForm').serialize(),
            success: function () {
                alert('Customer deleted successfully!');
                // You can optionally update the page or perform additional actions here
                // Navigate back to the customer list
                window.location.href = "/display_customer";
            },
            error: function () {
                alert('Error deleting customer.');
            }
        });
    }
    return false;
}
