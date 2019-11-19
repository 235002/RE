# Users login data
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mjg5NzcyMTEsImlhdCI6MTU2MDg1ODI5N30.xg2gFHZHte6f8oOIgED2Aw9jstwAEl3P0k4ABy2ry74"
admin_id = "28977211"
user_id = "28977211"

# Data to insert to DB
project_data = {
    "project": {
            "name": "Performance Testing",
            "short_description": "Prepare performance tests for web application.",
            "long_description": "Vulputate odio ut enim blandit volutpat maecenas",
            "number_of_members": 5,
            "technology": "Python, Locust",
            "tags": "WebDev, WebTest",
            "requirements": "none",
            "theme_color": "#3f51b5",
            "verified": 1},
    "token": token
}

news_data = {
    "news": {
            "title": "Need one person to my groupe!",
            "body": "Hi, I've just created new team, please be welcome to join me!",
            "user_id": user_id},
    "token": token
}

update_data = {
    "name": "Dominik",
    "surname": "Slawkowski",
    "team_id": None
}

# print codes and text function
def status(response):
    print("Resposne code:", response.status_code)
    print("Response plain text: ", response.text)

