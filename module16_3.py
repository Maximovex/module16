from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {1: 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_users():
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=5, max_length=15,
                                                 description='Enter your username', examples=['andrew'])],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter your age', examples=['20'])]):
    current_index = len(users) + 1
    users[current_index] = f'Имя:{username}, возраст: {age}'
    return f'User id: {current_index} is registered.'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples=['10'])],
                      username: Annotated[
                          str, Path(min_length=5, max_length=15,
                                    description='Enter your username', examples=['andrew'])],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter your age', examples=['20'])]):
    users[user_id] = f'Имя:{username}, возраст: {age}'
    return f'User id: {user_id} is updated.'


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples=['10'])]):
    users.pop(user_id)
    return f'User id: {user_id} is deleted.'
