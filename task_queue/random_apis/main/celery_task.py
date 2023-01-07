from celery import Celery
from random_apis.secret_key import get_secret_value


OFFICE_END_POINT = "https://officeapi.dev/api/quotes/random"

CHUCK_NORRIS_JOKE = "https://api.api-ninjas.com/v1/chucknorris?"
DAD_JOKE_END_POINT = "https://api.api-ninjas.com/v1/dadjokes"
DAD_JOKE_PARAMETERS = {
    "limit": 1
}
QUOTE_END_POINT = "https://api.api-ninjas.com/v1/quotes"
QUOTE_PARAMETERS = {
    "limit": 1
}

API_NINJA_API_KEY = {
    "X-Api-Key": get_secret_value('ninja_api_key')
}

PROGRAMING_JOKE_END_POINT = "https://v2.jokeapi.dev/joke/Programming"
PROGRAMING_JOKE_PARAMETERS = {
    "type": "twopart"
}


app = Celery("randomapis", broker="rabbitmq", backend="redis://redis:6379/0")


def send_tasks():
    responses = []

    office_api_task = app.send_task("request", (OFFICE_END_POINT,))
    chuck_joke_api_task = app.send_task("request", (CHUCK_NORRIS_JOKE, None, API_NINJA_API_KEY))
    dad_joke_api_task = app.send_task("request", (DAD_JOKE_END_POINT, DAD_JOKE_PARAMETERS, API_NINJA_API_KEY))
    quote_api_task = app.send_task("request", (QUOTE_END_POINT, QUOTE_PARAMETERS, API_NINJA_API_KEY))
    programming_joke_api_task = app.send_task("request", (PROGRAMING_JOKE_END_POINT, PROGRAMING_JOKE_PARAMETERS))

    responses.append(office_api_task.get())
    responses.append(chuck_joke_api_task.get())
    responses.append(dad_joke_api_task.get())
    responses.append(quote_api_task.get())
    responses.append(programming_joke_api_task.get())
    return responses
