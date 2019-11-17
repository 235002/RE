from locust import HttpLocust, TaskSet, between
import config


def login(l, client):
    l.client.post("/login", {"username": client['username'], "password": client['password']})


def logout(l, client):
    l.client.post("/logout", {"username": client['username'], "password": client['password']})


def index(l):
    l.client.get("/")


def profile(l):
    l.client.get("/profile")


class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def __init__(self):
        self.user = ''

    def set_user(self, user):
        self.user = user

    def get_user(self):
        return self.user

    def on_start(self):
        login(self, self.user)

    def on_stop(self):
        logout(self, self.user)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior()
    task_set.set_user(config.bjnovak)

    wait_time = between(5.0, 9.0)
