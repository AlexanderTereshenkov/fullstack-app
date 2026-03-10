from fastapi import APIRouter

router = APIRouter(prefix="/tickets", tags=["tickets"])

example_tickets = [{"name":"music fest", "desc":"cool fest"}, {"name":"games con", "desc":"cool games con"}]


@router.get("")
def get_all_tickets():
    '''
    Вывод всех билетов из БД с ограничением с помощью Query Parameters
    '''
    return example_tickets


@router.get("/{ticket_id}")
def get_ticket(ticket_id:int):
    '''
    Информация о конкретном билете, более подробная
    '''
    return {"result":f"ticket with id {ticket_id}"}

