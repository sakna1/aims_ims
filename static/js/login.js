function validateLogin() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (username === "" || password === "") {
        alert("Please enter related data");
        return false; // stop form submit
    }
    return true; // allow submit
}
