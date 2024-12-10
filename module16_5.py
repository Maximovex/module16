from fastapi import FastAPI, Path, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel

appi = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True}, debug=True)
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    user_id: int
    username: str
    age: int


users = []


@appi.get('/', response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@appi.get('/user/{userid}', response_class=HTMLResponse)
async def get_user(request: Request,
                   userid: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples=['10'])]):
    for i, user in enumerate(users):
        if user.user_id == userid:
            _id = i
            return templates.TemplateResponse('users.html', {'request': request, 'user': users[_id]})
    raise HTTPException(status_code=404, detail="User was not found")



@appi.post('/')
async def add_user(request:Request,username:str=Form(),age:int=Form()):
    userid=len(users)+1 if users else 1
    users.append(User(user_id=userid,username=username,age=age))
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@appi.put('/user/{userid}/{username}/{age}')
async def update_user(userid: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples=['10'])],
                      username: Annotated[str, Path(min_length=5, max_length=15, description='Enter your username',
                                                    examples=['andrew'])],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter your age', examples=['20'])]):
    for i, u in enumerate(users):
        if u.user_id == int(userid):
            users[i] = User(user_id=userid, username=username, age=age)
            return f'User id={userid} is updated.'

    raise HTTPException(status_code=404, detail="User was not found")


@appi.delete('/user/{userid}')
async def delete_user(userid: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples=['10'])]):
    for i, u in enumerate(users):
        if u.user_id == int(userid):
            users.pop(i)
            return f'User id: {userid} is deleted.'

    raise HTTPException(status_code=404, detail="User was not found")
