const alertMessage = document.getElementById('alert-message-error');

const message = alertMessage.dataset.message;
console.log(message)
if (message == "Email error") {
    alertMessage.style.display = 'block';
    alertMessage.textContent = "Email already used. Please try again with a different email."
}
if (message == "Password error") {
    alertMessage.style.display = 'block';
    alertMessage.textContent = "Password should contain atleast 8 characters."
}