from locust import HttpLocust, TaskSet, task
import json
import config


class InnoPointPerformanceTest(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.put("/user", {"token": config.token})
        config.status(response)

    # @task(1)
    # def admin_scenario(self):
    #     project_id = self.create_project(config.project_data)
    #     self.verify_project(project_id)
    #     self.delete_project(project_id)

    @task(1)
    def user_scenario(self):
        project_id = self.create_project(config.project_data)
        self.verify_project(project_id)

        team_id = self.create_team()
        self.post_news()

        self.join_team(team_id)
        self.join_project()

        self.leave_project(project_id)
        self.leave_team(config.user_id, config.update_data)

        self.delete_team(team_id)
        self.delete_project(project_id)

    def create_project(self, project_data):
        response = self.client.post("/projects", json=project_data)
        config.status(response)
        response = json.loads(response.text)
        return response[0]['id']

    def verify_project(self, project_id=1):
        self.client.put("/projects/verify/{0}".format(project_id), {"token": config.token})

    def create_team(self):
        team_data = {"team": {
                "open": 1,
                "max_number_of_members": 6,
                "token": config.token
            }
        }
        response = self.client.post("/teams", json=team_data)
        config.status(response)
        response = json.loads(response.text)
        return response[0]['team_id']

    def post_news(self):
        response = self.client.post("/news", config.news_data)
        config.status(response)

    def join_team(self, team_id=1):
        response = self.client.put("/teams/{0}/join".format(team_id), {"token": config.token})
        config.status(response)

    def join_project(self, project_id=1):
        response = self.client.put("/project/{0}/apply".format(project_id), {"token": config.token})
        config.status(response)

    def leave_project(self, project_id):
        response = self.client.put("/projects/{0}/leave".format(project_id), {"token": config.token})
        config.status(response)

    def leave_team(self, user_id, update_data):
        update_data = json.dumps(update_data)
        print(update_data)
        response = self.client.put("/users/{0}".format(user_id), json=update_data)
        config.status(response)

    def delete_team(self, team_id):
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
