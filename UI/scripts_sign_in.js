//alert("Javacript подключен");
const form = document.getElementById("auth_form");
const submit_auth_button = document.getElementById("submit_auth_button");

submit_auth_button.addEventListener("click", (e) => {
    e.preventDefault()
    const user = {
        mail: form.auth_email.value,
        password: form.auth_password.value
    }

    const url = `http://127.0.0.1:8000/users`;
    fetch(url, { method: 'GET', headers: { "Content-Type": "application/json" } })
        .then(res => res.json())
        .then(current_user => {
            for (let i = 0; i < current_user.length; i++) {
                if (current_user[i]["mail"] == user.mail && current_user[i]["password"] == user.password) {
                    console.log(current_user)
                    localStorage.setItem("user", JSON.stringify(current_user[i]))
                    window.location.href = "profile.html"
                }
            }
        })
        .catch(err => console.log(err))
})

const submit_registration_button = document.getElementById("submit_registration_button");

submit_registration_button.addEventListener("click", (e) => {
    e.preventDefault()
    if (form.registration_password.value == form.registration_password_check.value) {
        const user = {
            mail: form.registration_email.value,
            password: form.registration_password.value
        }
        console.log(user)

        const url = `http://127.0.0.1:8000/users${user["mail"]}?password=${user["password"]}&password_check=${form.registration_password_check.value}`;
        fetch(url, { method: 'POST', headers: { "Content-Type": "application/json" } })
            .then(res => res.json())
            .then(current_user => {
                console.log(current_user)
                localStorage.setItem("user", JSON.stringify(current_user))
                window.location.href = "profile.html"
            })
            .catch(err => console.log(err))
    }
})