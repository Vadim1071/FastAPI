from users.shema import UserSchema, UserGetSchema
from users.models import Base, UserModel
from database import sessionDep
from sqlalchemy import select

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Пользователи"]) # Хранит эндпоинты. Префикс - все эндпоинты будут начинаться с /users

@router.post('/', summary='Добавить пользователя', tags=['Пользователи'], response_model=UserGetSchema)   
async def add_user(new_user: UserSchema, session: sessionDep):
    new_user = UserModel(name=new_user.name, email=new_user.email)

    session.add(new_user)
    await session.commit()
    return new_user



@router.get('/', summary='Получить пользователей', tags=['Пользователи'], response_model=list[UserGetSchema])
async def get_users(session: sessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()    # Возвращается итератор. Поэтому нужно указать что конкретно показать (scalars().all())


@router.get("/{name}", response_model=UserSchema, summary='Конкретный пользователь', tags=['Пользователи'])
async def get_user(name: str, session: sessionDep):
    result = await session.execute(select(UserModel).where(UserModel.name==name)) #sql запрос. Селект из какой таблица по какому столбцу. Вернет строку (кортеж в ней)
    users = result.scalars.all() # преобразует в ОРМ объект. Только значения из колонок будут
    if not users:
        raise HTTPException(404)
    return users #возврат ОРМ объекта