const form = document.getElementById("create_project_form");
const submit_project_button = document.getElementById("submit_project_button");



submit_project_button.addEventListener("click", (e) => {
    e.preventDefault()

    project = {
        title: form.title.value
    }
    let current_user = JSON.parse(localStorage.getItem("user"))
    let current_category = JSON.parse(localStorage.getItem("category"))
    
    const url = `http://127.0.0.1:8000/projects?mail=${current_user["mail"]}&password=${current_user["password"]}&category_title=${current_category["title"]}&title=${project["title"]}`;
    fetch(url, { method: 'POST', headers: { "Content-Type": "application/json" } })
        .then(res => res.json())
        .then(project => {
            window.location.href = "profile.html"
        })
        .catch(err => console.log(err))
})