from fastapi import APIRouter
from schemas.users import User, UserUpdate, Creds
from schemas.categories import Task, Project, Category 
from services.users import user_service
import calendar
import uuid

router = APIRouter()

"""
@router.get(
    status_code=200,
)
def get_calendar():
    time = calendar.HTMLCalendar(firstweekday=0)
    time.formatyear(2023, width=3) 
    return calendar.formatyearpage(2023, 2, withyear=True)
"""
@router.get(
    "/users",
    status_code=200,
    response_model=list[User],
)
def get_users():
    return user_service.get_users()

@router.get(
    "/categories",
    status_code=200,
    response_model=list[Category],
)
def get_categories(mail: str,
                   password:str):
    creds: Creds = Creds(mail=mail,
                         password=password)
    return user_service.get_categories(creds)

@router.get(
    "/projects",
    status_code=200,
    response_model=list[Project],
)
def get_projects(category_id: str):
    return user_service.get_projects(category_id)

@router.get(
    "/tasks",
    status_code=200,
    response_model=list[Task],
)
def get_tasks(project_id: str):
    return user_service.get_tasks(project_id)

@router.get(
    "/tasks{author}",
    status_code=200,
    response_model=list[Task],
)
def get_tasks_from_another_users(mail: str):
    tasks = user_service.get_tasks_from_another_users(mail)
    print(tasks, 12)
    return tasks

@router.post("/users{mail}",
            status_code=200,
            response_model=User | str,)
def register(mail: str,
             password:str,
             password_check: str):
    if password == password_check:
        creds: Creds = Creds(mail=mail,
                    password=password) 
        user = user_service.register(creds=creds)
        return user
    return "Password mismatch"
         
"""
@router.post(
    "/users",
    status_code=200,
    response_model=User
)
def login(mail: str,
          password:str):
    creds: Creds = Creds(mail=mail,
                password=password)
    global current_users
    if user_service.login(creds) in current_users:
        return None
    current_users.append(user_service.login(creds))
    return user_service.login(creds)

    
@router.delete(
    "/users/{mail}",
    status_code=200
)
def unlogin(mail: str,
            password:str,):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    global current_users
    if user_service.login(creds) in current_users:
        return current_users.remove(user_service.login(creds))
    return False
"""    

@router.put(
    "/users/{id}",
    response_model=User,
)
def update_user(
        id: str,
        data: UserUpdate
):
    return user_service.update_user(payload=data, id=id)

@router.put(
    "/categories/{tasks}",
    status_code=200,
    response_model=Task,
)
def update_task_status(
        mail: str,
        task_title: str,
):
    return user_service.update_task_status(mail, task_title)

@router.post(
    "/categories",
    status_code=200,
    response_model=Category | str,
)
def create_category(
        mail: str,
        password:str,
        title: str,
        color: str
):
    creds: Creds = Creds(mail=mail,
                 password=password)
    category = user_service.create_category(creds, title, color)
    if category == None:
        return "This category is already exist"
    return category

@router.post(
    "/projects",
    status_code=200,
    response_model=Project | str,
)
def create_project(
        mail: str,
        password:str,
        category_title: str,
        title: str
):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    project = user_service.create_project(creds, category_title, title)
    if project == None:
        return "This project is already exist"
    return project

@router.post(
    "/tasks",
    status_code=200,
    response_model=Task | str,
)
def create_task(
        mail: str,
        password:str,
        category_title: str,
        project_title: str, 
        title: str, 
        urgent_color: str, 
        executor: str,
        comment: str,
        date: str
):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    task = user_service.create_task(creds, 
                                    category_title, 
                                    project_title, 
                                    title, 
                                    urgent_color, 
                                    mail, 
                                    executor,
                                    comment,
                                    date)
    if task == None:
        return "This task is already exist"
    return task

@router.delete(
    "/users/{categories}",
    status_code=200,
    response_model=Category,
)
def delete_category(
        mail: str,
        password:str,
        category_title: str
):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    return user_service.delete_category(creds, category_title)


@router.delete(
    "/categories",
    status_code=200,
    response_model=Project,
)
def delete_project(
        mail: str,
        password:str,
        category_title: str,
        project_title: str
):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    return user_service.delete_project(creds, category_title, project_title)

@router.delete(
    "/categories/{tasks}",
    status_code=200,
    response_model=Task,
)
def delete_task(
        mail: str,
        password:str,
        category_title: str,
        project_title: str,
        task_title: str,
):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    return user_service.delete_task(creds, category_title, project_title, task_title)
