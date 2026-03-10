#Личный кабинет польщзователя
from fastapi import APIRouter


router = APIRouter(prefix="/admin", tags=["admin"])


admin_tickets = [{"name":"music fest", "desc":"cool fest"}, {"name":"games con", "desc":"cool games con"}]


@router.get("/me")
def get_info():
    '''
    Получаем инфу про аккаунт и билеты, связанные с ним
    '''
    return {"name":"Name Surname", "info":"Info", "tickets":admin_tickets}


@router.post("/add_ticket")
def add_ticket():
    '''
    Добавляем билет в БД событий
    '''
    return {"event_name":"name", "event_date":"date", "event_desc":"description"}


@router.post("/delete_ticket/{ticket_id}")
def delete_ticket(ticket_id:int):
    '''
    Удаляем билет из БД событий
    '''
    return {"result":"delete event"}


@router.post("/update_ticket/{ticket_id}")
def update_ticket(ticket_id:int):
    '''
    Изменяем информацию о билете в БД
    '''
    return {"result":"update event"}