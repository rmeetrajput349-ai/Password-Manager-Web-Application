function togglePassword(id) {
    let field = document.getElementById(id);
    if (field.type === "password") {
        field.type = "text";
    } else {
        field.type = "password";
    }
}

function copyPassword(id) {
    let field = document.getElementById(id);
    field.select();
    navigator.clipboard.writeText(field.value);
    alert("Copied!");
}

function checkStrength() {
    let password = document.getElementById("password").value;
    let strengthText = document.getElementById("strength");

    if (password.length === 0) {
        strengthText.innerText = "";
        return;
    }

    let strength = 0;

    if (password.length >= 6) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[@$!%*?&]/)) strength++;

    if (strength <= 1) {
        strengthText.innerText = "Weak";
        strengthText.style.color = "red";
    } 
    else if (strength == 2 || strength == 3) {
        strengthText.innerText = "Medium";
        strengthText.style.color = "orange";
    } 
    else {
        strengthText.innerText = "Strong";
        strengthText.style.color = "green";
    }
}

function toggleSaved() {
    let section = document.getElementById("savedSection");

    if (section.style.display === "none") {
        section.style.display = "block";
    } else {
        section.style.display = "none";
    }
}

function changePassword(id) {
    document.getElementById("changeForm").style.display = "block";
    document.getElementById("recordId").value = id;
}