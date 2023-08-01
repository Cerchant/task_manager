//let year = current_user_tasks[k]["date"].spli("-")[0];
//let month = current_user_tasks[k]["date"].spli("-")[1];
function getDay(date) { // получить номер дня недели, от 0 (пн) до 6 (вс)
    let day = date.getDay();
    if (day == 0) day = 7; // сделать воскресенье (0) последним днем
    return day - 1;
}
function createCalendar(elem, year, month) {

    let mon = month - 1; // месяцы в JS идут от 0 до 11, а не от 1 до 12
    let d = new Date(year, mon);

    let table = '<table><tr><th>Mo</th><th>Tu</th><th>We</th><th>Th</th><th>Fr</th><th>Sa</th><th>Su</th></tr><tr>';

    // пробелы для первого ряда
    // с понедельника до первого дня месяца
    // * * * 1  2  3  4
    for (let i = 0; i < getDay(d); i++) {
        table += '<td></td>';
    }

    // <td> ячейки календаря с датами
    while (d.getMonth() == mon) {
        table += '<td>' + d.getDate() + '</td>';

        if (getDay(d) % 7 == 6) { // вс, последний день - перевод строки
            table += '</tr><tr>';
        }

        d.setDate(d.getDate() + 1);
    }

    // добить таблицу пустыми ячейками, если нужно
    // 29 30 31 * * * *
    if (getDay(d) != 0) {
        for (let i = getDay(d); i < 7; i++) {
            table += '<td></td>';
        }
    }

    // закрыть таблицу
    table += '</tr></table>';

    elem.innerHTML = table;
}


let current_user = JSON.parse(localStorage.getItem("user"))

//document.write(current_user["mail"])
const head = document.createElement("p");
head.innerText = current_user["mail"];
head.style.float = "right";


const mail = document.createElement("div");

mail.style.padding = "20px";
mail.style.borderRadius = "20px";
mail.style.background = "linear-gradient(to right, #eeeeee, #cccccc";
mail.style.width = "60%";
mail.style.float = "left";

const create_category_button = document.createElement("BUTTON");
create_category_button.innerHTML = "+Category";
//create_category_button.style = 3;

//create_category_button.style.top = "0";
//create_category_button.style.textAlign = "right";
create_category_button.style.padding = "10px";
create_category_button.style.borderRadius = "10px";
create_category_button.style.marginBottom = "10px";
create_category_button.style.background = "#eeeeee";
create_category_button.style.borderColor = "#eeeeee";


mail.innerText = "My Categories\n";
mail.appendChild(create_category_button);
mail.appendChild(head);



let tasks = [];

create_category_button.addEventListener('click', (e) => {
    e.preventDefault()
    create_category_button.onclick = function () {
        window.location.href = "create_category.html"
    };
});


const targetURL = `http://127.0.0.1:8000/categories?mail=${current_user["mail"]}&password=${current_user["password"]}`

fetch(targetURL, {
    method: 'GET', headers: {
        "Content-Type": "application/json"
    }
})
    .then(res => res.json())
    .then(current_user_categories => {
        for (let j = 0; j < current_user_categories.length; j++) {


            const category = document.createElement("div")
            category.innerHTML = current_user_categories[j]["title"]
            const create_project_button = document.createElement("BUTTON");
            create_project_button.innerHTML = "+Project";
            category.appendChild(create_project_button);

            category.style.padding = "20px";
            category.style.borderRadius = "20px";
            category.style.marginBottom = "10px";
            category.style.width = "75%";
            console.log(current_user_categories[j]["color"]);
            category.style.background = "linear-gradient(to right, #eeeeee 90%, " +
                current_user_categories[j]["color"] + " 10%)";

            create_project_button.style.padding = "10px";
            create_project_button.style.borderRadius = "10px";
            create_project_button.style.marginBottom = "10px";
            create_project_button.style.background = "#eeeeee";
            create_project_button.style.borderColor = "#eeeeee";

            create_project_button.addEventListener('click', (e) => {
                e.preventDefault()
                create_project_button.onclick = function () {
                    localStorage.setItem("category", JSON.stringify(current_user_categories[j]))
                    console.log(localStorage.getItem("category"));
                    window.location.href = "create_project.html"
                };
            });

            const delete_category_button = document.createElement("BUTTON");
            delete_category_button.innerHTML = "Delete Category";
            category.appendChild(delete_category_button);

            delete_category_button.style.padding = "10px";
            delete_category_button.style.borderRadius = "10px";
            delete_category_button.style.marginBottom = "10px";
            delete_category_button.style.background = "#eeeeee";
            delete_category_button.style.borderColor = "#eeeeee";

            delete_category_button.addEventListener('click', (e) => {
                e.preventDefault()
                delete_category_button.onclick = function () {
                    const url = `http://127.0.0.1:8000/users/{categories}?mail=${current_user["mail"]}&password=${current_user["password"]}&category_title=${current_user_categories[j]["title"]}`;
                    fetch(url, { method: 'DELETE', headers: { "Content-Type": "application/json" } })
                        .then(res => res.json())
                        .then(task => {
                            window.location.href = "profile.html"
                        })
                        .catch(err => console.log(err))
                };

            });

            const url = `http://127.0.0.1:8000/projects?category_id=${current_user_categories[j]["id"]}`;
            fetch(url, { method: 'GET', headers: { "Content-Type": "application/json" } })
                .then(res => res.json())
                .then(current_user_projects => {
                    for (let i = 0; i < current_user_projects.length; i++) {
                        let project = document.createElement("ul")
                        project.innerHTML = current_user_projects[i]["title"]
                        project.style.paddingLeft = "30px";
                        project.style.borderRadius = "10px";
                        project.style.marginBottom = "10px";
                        project.style.width = "75%";

                        const create_task_button = document.createElement("BUTTON");
                        create_task_button.innerHTML = "+Task";
                        project.appendChild(create_task_button);

                        create_task_button.style.padding = "10px";
                        create_task_button.style.borderRadius = "10px";
                        create_task_button.style.marginBottom = "10px";
                        create_task_button.style.background = "#eeeeee";
                        create_task_button.style.borderColor = "#eeeeee";

                        create_task_button.addEventListener('click', (e) => {
                            e.preventDefault()
                            create_task_button.onclick = function () {
                                localStorage.setItem("category", JSON.stringify(current_user_categories[j]))
                                localStorage.setItem("project", JSON.stringify(current_user_projects[i]))
                                console.log(localStorage.getItem("project"));
                                window.location.href = "create_task.html"
                            };
                        });


                        const delete_project_button = document.createElement("BUTTON");
                        delete_project_button.innerHTML = "Delete Project";
                        project.appendChild(delete_project_button);

                        delete_project_button.style.padding = "10px";
                        delete_project_button.style.borderRadius = "10px";
                        delete_project_button.style.marginBottom = "10px";
                        delete_project_button.style.background = "#eeeeee";
                        delete_project_button.style.borderColor = "#eeeeee";

                        delete_project_button.addEventListener('click', (e) => {
                            e.preventDefault()
                            delete_project_button.onclick = function () {
                                const url = `http://127.0.0.1:8000/categories?mail=${current_user["mail"]}&password=${current_user["password"]}&category_title=${current_user_categories[j]["title"]}&project_title=${current_user_projects[i]["title"]}`;
                                fetch(url, { method: 'DELETE', headers: { "Content-Type": "application/json" } })
                                    .then(res => res.json())
                                    .then(task => {
                                        window.location.href = "profile.html"
                                    })
                                    .catch(err => console.log(err))
                            };

                        });

                        const url = `http://127.0.0.1:8000/tasks?project_id=${current_user_projects[i]["id"]}`;
                        fetch(url, { method: 'GET', headers: { "Content-Type": "application/json" } })
                            .then(res => res.json())
                            .then(current_user_tasks => {
                                let task_for_calendar = [];
                                for (let k = 0; k < current_user_tasks.length; k++) {
                                    let task = document.createElement("li")
                                    let task_span = document.createElement("span")
                                    let filling = document.createElement("div")

                                    task_span.innerText = current_user_tasks[k]["title"]

                                    const delete_task_button = document.createElement("BUTTON");
                                    delete_task_button.innerHTML = "Delete Task";

                                    delete_task_button.style.padding = "10px";
                                    delete_task_button.style.borderRadius = "10px";
                                    delete_task_button.style.marginBottom = "10px";
                                    delete_task_button.style.background = "#eeeeee";
                                    delete_task_button.style.borderColor = "#eeeeee";

                                    delete_task_button.addEventListener('click', (e) => {
                                        e.preventDefault()
                                        delete_task_button.onclick = function () {
                                            const url = `http://127.0.0.1:8000/categories/{tasks}?mail=${current_user["mail"]}&password=${current_user["password"]}&category_title=${current_user_categories[j]["title"]}&project_title=${current_user_projects[i]["title"]}&task_title=${current_user_tasks[k]["title"]}`;
                                            fetch(url, { method: 'DELETE', headers: { "Content-Type": "application/json" } })
                                                .then(res => res.json())
                                                .then(task => {
                                                    window.location.href = "profile.html"
                                                })
                                                .catch(err => console.log(err))
                                        };

                                    });
                                    if (current_user_tasks[k]["executor"] == current_user["mail"] && current_user_tasks[k]["status"] == "in process") {
                                        const execute_task_button = document.createElement("BUTTON");
                                        execute_task_button.innerHTML = "Execute";

                                        execute_task_button.style.padding = "10px";
                                        execute_task_button.style.borderRadius = "10px";
                                        execute_task_button.style.marginBottom = "10px";
                                        execute_task_button.style.background = "#eeeeee";
                                        execute_task_button.style.borderColor = "#eeeeee";

                                        execute_task_button.addEventListener('click', (e) => {
                                            e.preventDefault()
                                            execute_task_button.onclick = function () {
                                                const url = `http://127.0.0.1:8000/categories/{tasks}?mail=${current_user["mail"]}&task_title=${current_user_tasks[k]["title"]}`;
                                                fetch(url, { method: 'PUT', headers: { "Content-Type": "application/json" } })
                                                    .then(res => res.json())
                                                    .then(task => {
                                                        window.location.href = "profile.html"
                                                    })
                                                    .catch(err => console.log(err))
                                            };

                                        });
                                        task_span.appendChild(execute_task_button);
                                    }
                                    task_span.appendChild(delete_task_button);

                                    filling.innerText = "\nExecutor: " + current_user_tasks[k]["executor"] +
                                        "\nDate: " + current_user_tasks[k]["date"] +
                                        "\n\n" + current_user_tasks[k]["comment"] +
                                        "\n\n" + current_user_tasks[k]["status"]

                                    filling.style.paddingLeft = "30px";
                                    task_span.appendChild(filling)

                                    task.style.paddingLeft = "30px";
                                    task.style.color = current_user_tasks[k]["urgent_color"];
                                    task_span.style.color = "black";

                                    task_for_calendar = [current_user_categories[j]["color"],
                                    current_user_tasks[k]["urgent_color"],
                                    current_user_tasks[k]["date"]];

                                    task.appendChild(task_span)
                                    project.appendChild(task)
                                }
                            })
                            .catch(err => console.log(err))


                        category.appendChild(project)
                    }

                    mail.appendChild(category)
                })
                .catch(err => console.log(err))

        }


    }
    ).catch(err => console.log(err))


const right = document.createElement("div");

right.style.padding = "20px";
right.style.borderRadius = "20px";
right.style.marginBottom = "10px";
right.style.background = "#eeeeee";
right.style.background = "linear-gradient(to right, #eeeeee, #cccccc";
right.style.width = "33%";

let calendar = document.createElement("p");
createCalendar(calendar, 2023, 3);
right.style.float = "right";
calendar.style.textAlign = "center";

right.appendChild(calendar);

const tasks_from_another_users = document.createElement("ul");

tasks_from_another_users.innerText = "Tasks from another users";

tasks_from_another_users.style.padding = "20px";
tasks_from_another_users.style.borderRadius = "20px";
tasks_from_another_users.style.background = "linear-gradient(to right, #eeeeee, #cccccc";
tasks_from_another_users.style.width = "33%";
tasks_from_another_users.style.float = "right";

const url = `http://127.0.0.1:8000/tasks{author}?mail=${current_user["mail"]}`;
fetch(url, { method: 'GET', headers: { "Content-Type": "application/json" } })
    .then(res => res.json())
    .then(current_user_tasks => {
        for (let k = 0; k < current_user_tasks.length; k++) {
            let task_from_another_users = document.createElement("li")
            let task_from_another_users_span = document.createElement("span")
            let filling_from_another_users = document.createElement("div")

            task_from_another_users_span.innerText = current_user_tasks[k]["title"]


            const execute_task_from_another_users_button = document.createElement("BUTTON");
            execute_task_from_another_users_button.innerHTML = "Execute";

            execute_task_from_another_users_button.style.padding = "10px";
            execute_task_from_another_users_button.style.borderRadius = "10px";
            execute_task_from_another_users_button.style.marginBottom = "10px";
            execute_task_from_another_users_button.style.background = "#eeeeee";
            execute_task_from_another_users_button.style.borderColor = "#eeeeee";

            if (current_user_tasks[k]["status"] == "in process") {
                execute_task_from_another_users_button.addEventListener('click', (e) => {
                    e.preventDefault()
                    execute_task_from_another_users_button.onclick = function () {
                        const url = `http://127.0.0.1:8000/categories/{tasks}?mail=${current_user["mail"]}&task_title=${current_user_tasks[k]["title"]}`;
                        fetch(url, { method: 'PUT', headers: { "Content-Type": "application/json" } })
                            .then(res => res.json())
                            .then(task => {
                                window.location.href = "profile.html"
                            })
                            .catch(err => console.log(err))
                    };

                });
                task_from_another_users_span.appendChild(execute_task_from_another_users_button);
            }

            filling_from_another_users.innerText = "\nAuthor: " + current_user_tasks[k]["author"] +
                "\nDate: " + current_user_tasks[k]["date"] +
                "\n\n" + current_user_tasks[k]["comment"] +
                "\n\n" + current_user_tasks[k]["status"]

            filling_from_another_users.style.paddingLeft = "30px";
            task_from_another_users_span.appendChild(filling_from_another_users)

            task_from_another_users.style.paddingLeft = "30px";
            console.log(current_user_tasks[k]);
            task_from_another_users.style.color = current_user_tasks[k]["urgent_color"];
            task_from_another_users_span.style.color = "black";

            task_from_another_users.appendChild(task_from_another_users_span)
            tasks_from_another_users.appendChild(task_from_another_users)
        }
    })
    .catch(err => console.log(err))

document.body.appendChild(mail);
document.body.appendChild(right);
document.body.appendChild(tasks_from_another_users);
