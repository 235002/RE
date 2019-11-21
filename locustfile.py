from locust import HttpLocust, TaskSet, task
import json
import config


class InnoPointPerformanceTest(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.put("/user", {"token": config.token})
        config.status(response)

    @task(1)
    def admin_scenario(self):
        project_id = self.create_project(config.project_data)
        self.verify_project(project_id)
        self.delete_project(project_id)

    @task(1)
    def user_scenario(self):
        project_id = self.create_project(config.project_data)
        self.verify_project(project_id)

        team_id = self.create_team(config.team_data)
        self.post_news()

        self.join_project(project_id)

        self.leave_project(project_id)
        self.leave_team(team_id)

        self.delete_project(project_id)

    @task(1)
    def create_project(self, project_data=config.project_data):
        response = self.client.post("/projects", json=project_data)
        config.status(response)
        response = json.loads(response.text)
        return response[0]['id']

    def verify_project(self, project_id=1):
        self.client.put("/projects/verify/{0}".format(project_id), {"token": config.token})

    @task(3)
    def get_teams(self):
        response = self.client.put("/teams", {"token": config.token})
        config.status(response)

    @task(4)
    def get_team(self, team_id=3):
        response = self.client.get("/teams/{0}".format(team_id))
        config.status(response)

    @task(4)
    def get_projects(self):
        response = self.client.put("/projects", {"token": config.token})
        config.status(response)

    @task(4)
    def get_project(self, project_id=1):
        response = self.client.get("/projects/{0}".format(project_id))
        config.status(response)

    @task(4)
    def get_user(self):
        response = self.client.put("/user", {"token": config.token})
        config.status(response)

    @task(4)
    def get_users(self):
        response = self.client.put("/users", {"token": config.token})
        config.status(response)

    @task(2)
    def change_team_status(self, team_id=2):
        response = self.client.put("/teams/{0}/status".format(team_id), {"token": config.token, "status": 1})
        config.status(response)

    @task(3)
    def create_team(self, team_data=config.team_data):
        response = self.client.post("/teams", json=team_data)
        config.status(response)
        return int(response.text)

    @task(2)
    def post_news(self, news_data=config.news_data):
        response = self.client.post("/news", news_data)
        config.status(response)

    def join_project(self, project_id=1):
        response = self.client.put("/projects/apply/{0}".format(project_id), {"token": config.token})
        config.status(response)

    def leave_project(self, project_id):
        response = self.client.put("/projects/{0}/leave".format(project_id), {"token": config.token})
        config.status(response)

    def leave_team(self, team_id):
        response = self.client.delete("/teams/{0}".format(team_id))
        config.status(response)

    def delete_project(self, project_id):
        response = self.client.delete("/projects/{0}".format(project_id))
        config.status(response)


class WebsiteUser(HttpLocust):
    task_set = InnoPointPerformanceTest
    host = "http://localhost:3030"
    min_wait = 2 * 1000
    max_wait = 6 * 1000
