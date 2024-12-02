from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return 'Главная страница'

@app.get('/user/admin')
async def admin():
    return 'Вы вошли как администратор'

@app.get('/user/{user_id}')
async def user(user_id):
    return f'Вы вошли как пользователь {user_id}'

@app.get('/user')
async def user_params(username:str,age:int):
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
