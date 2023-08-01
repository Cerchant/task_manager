const form = document.getElementById("create_task_form");
const submit_task_button = document.getElementById("submit_task_button");



submit_task_button.addEventListener("click", (e) => {
    e.preventDefault()
    let urgent_color = ""
    if (form.urgent_color.value == "very urgent (red)"){
        urgent_color = "red"
    }
    else if (form.urgent_color.value == "urgently (orange)"){
        urgent_color = "orange"
    }
    else if (form.urgent_color.value == "can wait (yellow)"){
        urgent_color = "yellow"
    }
    else if (form.urgent_color.value == "not urgent (green)"){
        urgent_color = "green"
    }
    console.log(urgent_color)
    task = {
        title: form.title.value,
        urgent_color: urgent_color,
        executor: form.executor.value,
        comment: form.comment.value,
        date: form.date.value,
    }
    console.log(task)
    let current_user = JSON.parse(localStorage.getItem("user"))
    let current_category = JSON.parse(localStorage.getItem("category"))
    let current_project = JSON.parse(localStorage.getItem("project"))

    const url = `http://127.0.0.1:8000/tasks?mail=${current_user["mail"]}&password=${current_user["password"]}&category_title=${current_category["title"]}&project_title=${current_project["title"]}&title=${task["title"]}&urgent_color=${task["urgent_color"]}&executor=${task["executor"]}&comment=${task["comment"]}&date=${task["date"]}&status=in_process`;
    fetch(url, { method: 'POST', headers: { "Content-Type": "application/json" } })
        .then(res => res.json())
        .then(task => {
            window.location.href = "profile.html"
        })
        .catch(err => console.log(err))
})