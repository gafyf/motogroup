$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })


var form = document.getElementById('form_id');

form.addEventListener('submit', function(event) {
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    // form.classList.add('was-validated');
    form.addClass('was-validated');
})

var nameField = document.getElementById("id_username");
    if (!nameField.checkValidity()) {
        nameField.classList.add("is-invalid");
        formFlag = false;
    }
