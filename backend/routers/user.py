#Личный кабинет польщзователя
from fastapi import APIRouter


router = APIRouter(prefix="/user", tags=["user"])

example_tickets = [{"name":"music fest", "desc":"cool fest"}, {"name":"games con", "desc":"cool games con"}]


@router.get("/me")
def get_info():
    '''
    Получаем инфу про аккаунт и билеты, связанные с ним
    '''
    return {"name":"Name Surname", "info":"Info", "tickets":example_tickets}


@router.post("/add_ticket/{ticket_id}")
def add_ticket(ticket_id:int):
    '''
    Добавляем билет в БД юзера
    '''
    return {"result":"added ticket"}


@router.post("/delete_ticket/{ticket_id}")
def delete_ticket(ticket_id:int):
    '''
    Удаляем билет из БД юзера
    '''
    return {"result":"delete ticket"}


@router.post("/qr")
def create_qr():
    '''
    Создаем QR на сервере возвращаем пользователю
    '''
    return {"result":"QR IMAGE"}
