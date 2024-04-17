function validatePassword(){
    var password = document.getElementById("password"),
        confirm_password = document.getElementById("confirm_password"),
        error_message = document.getElementById("error-message");

    if(password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Les mots de passe ne correspondent pas");
        error_message.textContent = "Les mots de passe ne correspondent pas";
    } else {
        confirm_password.setCustomValidity('');
        error_message.textContent = "";
    }
}
window.onload = function() {
    document.getElementById("password").onchange = validatePassword;
    document.getElementById("confirm_password").onkeyup = validatePassword;
}