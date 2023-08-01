const form = document.getElementById("create_category_form");
const submit_category_button = document.getElementById("submit_category_button");



submit_category_button.addEventListener("click", (e) => {
    e.preventDefault()

    category = {
        title: form.title.value,
        color: form.color.value
    }
    category_color = "%23" + category["color"].split("#")["1"]
    let current_user = JSON.parse(localStorage.getItem("user"))

    const url = `http://127.0.0.1:8000/categories?mail=${current_user["mail"]}&password=${current_user["password"]}&title=${category["title"]}&color=${category_color}`;
    fetch(url, { method: 'POST', headers: { "Content-Type": "application/json" } })
        .then(res => res.json())
        .then(category => {
            window.location.href = "profile.html"
        })
        .catch(err => console.log(err))
})