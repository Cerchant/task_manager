from schemas.users import User, UserUpdate, Creds
from schemas.categories import Category, Project, Task
import uuid
import json
import re
import copy


class UserService:
    def __init__(self) -> None:
        ...
    
    def _valid_mail(self, mail: str) -> bool:
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

        if re.match(pattern, mail) is not None:
            return True
        else:
            return False

    def get_users(self) -> list[User]:
        with open('data/user_data.json') as file:
            self.data = json.load(file)
        users = []

        for item in self.data["users"]:
            users.append(
                User(
                    id=item["id"],
                    mail=item["mail"],
                    password=item["password"],
                    categories=item["categories"]
                )
            )

        return users
    
    def get_categories(self, creds: Creds) -> list[Category]:
        with open('data/user_data.json') as user_file:
            self.user_data = json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data = json.load(category_file)
        categories = []

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for category in self.category_data["categories"]:
                    if (category["id"] in user["categories"]):
                        categories.append(
                            Category(
                                id=category["id"],
                                projects=category["projects"],
                                title=category["title"],
                                color=category["color"]
                        )
                    )
        return categories
    
    def get_projects(self, category_id: str) -> list[Project]:
        with open('data/category_data.json') as category_file:
            self.category_data = json.load(category_file)
        projects = []
        for category in self.category_data["categories"]:
            if category_id == category["id"]:
                for project in self.category_data["projects"]:
                    if (project["id"] in category["projects"]):
                        projects.append(Project(
                            id=project["id"],
                            tasks=project["tasks"],
                            title=project["title"],
                            )
                        ) 
                return projects
            
    def get_tasks(self, project_id: str) -> list[Task]:
        with open('data/category_data.json') as category_file:
            self.category_data = json.load(category_file)
        tasks = []
        for project in self.category_data["projects"]:
            if project_id == project["id"]:
                for task in self.category_data["tasks"]:
                    if (task["id"] in project["tasks"]):
                        tasks.append(Task(
                                        id=task["id"],
                                        title=task["title"],
                                        urgent_color=task["urgent_color"],
                                        author = task["author"], 
                                        executor = task["executor"],
                                        comment = task["comment"],
                                        date = task["date"],
                                        status = task["status"] 
                                    )
                        ) 
                return tasks
            
    def get_tasks_from_another_users(self, mail: str) -> list[Task]:
        with open('data/category_data.json') as category_file:
            self.category_data = json.load(category_file)
        tasks = []

        for task in self.category_data["tasks"]:
            if (task["executor"] == mail) and (task["author"] != mail):
                tasks.append(Task(
                    id=task["id"],
                    title=task["title"],
                    urgent_color=task["urgent_color"],
                    author = task["author"], 
                    executor = task["executor"],
                    comment = task["comment"],
                    date = task["date"],
                    status = task["status"] 
                    )
                )
        return tasks

    def update_user(self, id: uuid.UUID, creds: UserUpdate) -> User:
        if auth_user := self._auth(creds.auth):
            if auth_user.id != id:
                raise ValueError()
            
            with open('data/user_data.json') as file:
                self.data = json.load(file)

            for user in self.data["users"]:
                if user["id"] == str(id):
                    user["mail"] = creds.mail
                    with open('data/user_data.json', "w") as file:
                        json.dump(self.data, file, indent=2, ensure_ascii=False)
                    return User(
                        id=user["id"],
                        mail=user["mail"],
                        password=user["password"],
                        categories=user["categories"]
                    )

        raise ValueError()
    
    def update_task_status(self, mail: str, task_title: str) -> Task:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)

        for task in self.category_data["tasks"]:
            if (task_title == task["title"]) and (mail == task["executor"]):
                if task["status"] == "in process":
                    task["status"] = "done"
                else:
                    task["status"] = "in process"

        with open('data/user_data.json', "w") as user_file:
            json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
        with open('data/category_data.json', "w") as category_file:
            json.dump(self.category_data, category_file, indent=2, ensure_ascii=False)

        return Task(
            id=task["id"],
            title=task["title"],
            urgent_color=task["urgent_color"],
            author = task["author"], 
            executor = task["executor"],
            comment = task["comment"],
            date = task["date"],
            status = task["status"] 
        )


    def _auth(self, creds: Creds) -> User | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        for user in self.user_data["users"]:
            if user["mail"] == creds.mail and user["password"] == creds.password:
                return User(
                    id=user["id"],
                    mail=user["mail"],
                    password=user["password"],
                    categories=user["categories"]
                )
        return None
    
    def register(self, creds: Creds) -> User | str:
        if self._valid_mail(creds.mail) == False:
            return "Uncorrect email form"
        if self._auth(creds):
            return None
        with open('data/user_data.json') as file:
            self.data=json.load(file)
        user = {
            "id": str(uuid.uuid4()),
            "mail": creds.mail,
            "password": creds.password,
            "categories": []
        }
        self.data["users"].append(user)
        with open('data/user_data.json', "w") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)
        return User(
            id=user["id"],
            mail=user["mail"],
            password=user["password"],
            categories=user["categories"]
        )
    
    def _category_exist(self, creds: Creds, category_title: str) -> Category | None:
        with open('data/user_data.json') as user_file:
            self.data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)
        
        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for category in self.category_data["categories"]:
                    if (category["title"] == category_title) and (category["id"] in user["categories"]):
                        return Category(
                            id=category["id"],
                            projects=category["projects"],
                            title=category["title"],
                            color=category["color"]
                        )
        return None
    
    def _project_exist(self, creds: Creds, category_title: str, project_title: str) -> Project | None:
        with open('data/user_data.json') as user_file:
            self.data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)
        
        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for category in self.category_data["categories"]:
                    if (category["title"] == category_title) and (category["id"] in user["categories"]):
                        for project in self.category_data["projects"]:
                                if (project_title == project["title"] and project["id"] in category["projects"]):
                                    return Project(
                                        id=project["id"],
                                        tasks=project["tasks"],
                                        title=project["title"],
                                    )
        return None
    
    def _task_exist(self, creds: Creds, category_title: str, project_title: str, task_title: str) -> Task | None:
        with open('data/user_data.json') as user_file:
            self.data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)
        
        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for category in self.category_data["categories"]:
                    if (category["title"] == category_title) and (category["id"] in user["categories"]):
                        for project in self.category_data["projects"]:
                                if (project_title == project["title"]):
                                    for task in self.category_data["tasks"]:
                                        if (task_title == task["title"]) and (task["id"] in project["tasks"]):
                                            return Task(
                                                id=task["id"],
                                                title=task["title"],
                                                urgent_color=task["urgent_color"],
                                                author = task["author"], 
                                                executor = task["executor"],
                                                comment = task["comment"],
                                                date = task["date"],
                                                status = task["status"] 
                                            )
        return None
    
    def login(self, creds: Creds) -> User:
        auth_user = self._auth(creds)
        if auth_user == None:
            return "User is not found"
        return auth_user
    
    def create_category(self, creds: Creds, category_title: str, color: str) -> Category | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)

        
        check_category = self._category_exist(creds, category_title)
        if check_category == None:
            category = {
                        "id": str(uuid.uuid4()),
                        "projects": [],
                        "title": category_title,
                        "color": color
            }
            for user in self.user_data["users"]:
                if user["mail"] == creds.mail and user["password"] == creds.password:
                    user["categories"].append(str(category["id"]))
                    self.category_data["categories"].append(category)

                    with open('data/user_data.json', "w") as user_file:
                        json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                    with open('data/category_data.json', "w") as category_file:
                        json.dump(self.category_data, category_file, indent=2, ensure_ascii=False)
                    return Category(
                        id=category["id"],
                        projects=category["projects"],
                        title=category["title"],
                        color=category["color"]
                    )
        return None
        
    def create_project(self, creds: Creds, category_title: str, project_title: str) -> Project:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)
        
        check_project = self._project_exist(creds, category_title, project_title)
        print(check_project, "true")
        if check_project == None:
            project = {
                        "id": str(uuid.uuid4()),
                        "tasks": [],
                        "title": project_title
            }
            for user in self.user_data["users"]:
                if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                    for category in self.category_data["categories"]:
                        if  (category["title"] == category_title) and (category["id"] in user["categories"]):
                            category["projects"].append(str(project["id"]))
                            self.category_data["projects"].append(project)

                            with open('data/user_data.json', "w") as user_file:
                                json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                            with open('data/category_data.json', "w") as category_file:
                                json.dump(self.category_data, category_file, indent=2, ensure_ascii=False)
                            print(project)
                            return Project(
                                id=project["id"],
                                tasks=project["tasks"],
                                title=project["title"]
                            )
        return None

    def create_task(self, creds: Creds, 
                    category_title: str, 
                    project_title: str, 
                    task_title: str, 
                    urgent_color: str, 
                    author: str, 
                    executor: str,
                    comment: str,
                    date: str) -> Task:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)

        check_task = self._task_exist(creds, category_title, project_title, task_title)
        if check_task == None:
            task = {
                        "id": str(uuid.uuid4()),
                        "title": task_title,
                        "urgent_color": urgent_color,
                        "author": author, 
                        "executor": executor,
                        "comment": comment,
                        "date": date,
                        "status": "in process"
            }
            for user in self.user_data["users"]:
                if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                    for category in self.category_data["categories"]:
                        if (category["title"] == category_title) and (category["id"] in user["categories"]):
                            for project in self.category_data["projects"]:
                                if (project["title"] == project_title) and (project["id"] in category["projects"]):
                                    project["tasks"].append(str(task["id"]))
                                    self.category_data["tasks"].append(task)

                                    with open('data/user_data.json', "w") as user_file:
                                        json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                                    with open('data/category_data.json', "w") as category_file:
                                        json.dump(self.category_data, category_file, indent=2, ensure_ascii=False)
                                    return Task(
                                        id=task["id"],
                                        title=task["title"],
                                        urgent_color=task["urgent_color"],
                                        author = task["author"], 
                                        executor = task["executor"],
                                        comment = task["comment"],
                                        date = task["date"],
                                        status = task["status"] 
                                    )
            
    def delete_category(self, creds: Creds, category_title: str) -> Category:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)

        new_category_data = copy.deepcopy(self.category_data)

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail and user["password"] == creds.password):
                for category in self.category_data["categories"]:
                    if (category["title"] == category_title) and (category["id"] in user["categories"]):
                        for project in self.category_data["projects"]:
                            if project["id"] in category["projects"]:
                                new_category_data["projects"].remove(project)
                                for task in self.category_data["tasks"]:
                                    if (task["id"] in project["tasks"]):
                                        project["tasks"].remove(task["id"])
                                        new_category_data["tasks"].remove(task)
                                category["projects"].remove(project["id"])
                                
                        self.category_data["projects"] = new_category_data["projects"]
                        self.category_data["tasks"] = new_category_data["tasks"]

                        user["categories"].remove(category["id"])
                        self.category_data["categories"].remove(category)
                        with open('data/user_data.json', "w") as user_file:
                            json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                        with open('data/category_data.json', "w") as category_file:
                            json.dump(self.category_data, category_file, indent=2, ensure_ascii=False)

                        return Category(
                            id=category["id"],
                            projects=category["projects"],
                            title=category["title"],
                            color=category["color"]
                        )
    
    def delete_project(self, creds: Creds, category_title: str, project_title: str) -> Project:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail and user["password"] == creds.password):
                for category in self.category_data["categories"]:
                    if (category["title"] == category_title) and (category["id"] in user["categories"]):
                        for project in self.category_data["projects"]:
                            if (project["id"] in category["projects"]) and (project_title == project["title"]):
                                new_category_data = copy.deepcopy(self.category_data)
                                for task in self.category_data["tasks"]:
                                    if (task["id"] in project["tasks"]):
                                        new_category_data["tasks"].remove(task)
                                        project["tasks"].remove(task["id"])
                                    print(project)
                                self.category_data["tasks"] = new_category_data["tasks"]
                                category["projects"].remove(project["id"])
                                self.category_data["projects"].remove(project)
                                with open('data/user_data.json', "w") as user_file:
                                    json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                                with open('data/category_data.json', "w") as category_file:
                                    json.dump(self.category_data, category_file, indent=2, ensure_ascii=False)

                                return Project(
                                    id=project["id"],
                                    tasks=project["tasks"],
                                    title=project["title"],
                                )

    def delete_task(self, creds: Creds, category_title: str, project_title: str, task_title: str) -> Task:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/category_data.json') as category_file:
            self.category_data=json.load(category_file)

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail and user["password"] == creds.password):
                for category in self.category_data["categories"]:
                    if (category["title"] == category_title) and (category["id"] in user["categories"]):
                        for project in self.category_data["projects"]:
                            if (project["id"] in category["projects"]) and (project_title == project["title"]):
                                for task in self.category_data["tasks"]:
                                    if (task_title == task["title"]) and (task["id"] in project["tasks"]):
                                        project["tasks"].remove(task["id"])
                                        self.category_data["tasks"].remove(task)
                                        with open('data/user_data.json', "w") as user_file:
                                            json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                                        with open('data/category_data.json', "w") as category_file:
                                            json.dump(self.category_data, category_file, indent=2, ensure_ascii=False)

                                        return Task(
                                            id=task["id"],
                                            title=task["title"],
                                            urgent_color=task["urgent_color"],
                                            author = task["author"], 
                                            executor = task["executor"],
                                            comment = task["comment"],
                                            date = task["date"],
                                            status = task["status"] 
                                        )
                            
      
user_service: UserService = UserService()