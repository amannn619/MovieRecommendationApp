const alertMessage = document.getElementById('alert-message-error');
const successMessage = document.getElementById('alert-message-success');


const message = alertMessage.dataset.message;
if (message == "Email error") {
    alertMessage.style.display = 'block';
    alertMessage.textContent = "Email does not exist.";
}
if (message == "Password error") {
    alertMessage.style.display = 'block';
    alertMessage.textContent = "Wrong password.";
}
if (message == "Registration Success") {
    successMessage.style.display = "block"
}