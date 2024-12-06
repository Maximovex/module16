from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    user_id: int
    username: str
    age: int


users = []


@app.get('/users')
async def get_users():
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=5, max_length=15,
                                                 description='Enter your username', examples=['andrew'])],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter your age', examples=['20'])]):
    current_index = max(user.user_id for user in users) + 1 if users else 1
    user = User(user_id=current_index, username=username, age=age)
    users.append(user)
    return f'Пользователь id = {user.user_id} добавлен.'


@app.put('/user/{userid}/{username}/{age}')
async def update_user(userid: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples=['10'])],
                      username:Annotated[str, Path(min_length=5, max_length=15,description='Enter your username', examples=['andrew'])],
                      age:Annotated[int, Path(ge=18, le=120, description='Enter your age', examples=['20'])]):

    for i, u in enumerate(users):
        if u.user_id == int(userid):
            users[i] = User(user_id=userid, username=username, age=age)
            return f'User id={userid} is updated.'


    raise HTTPException(status_code=404, detail="User was not found")



@app.delete('/user/{userid}')
async def delete_user(userid:Annotated[int, Path(ge=1, le=100, description='Enter user id', examples=['10'])]):

    for i, u in enumerate(users):
        if u.user_id == int(userid):
            users.pop(i)
            return f'User id: {userid} is deleted.'

    raise HTTPException(status_code=404, detail="User was not found")


