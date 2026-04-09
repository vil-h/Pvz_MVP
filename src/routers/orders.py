from fastapi import APIRouter, HTTPException, status
from src.database.db_utils import get_connection, close_connection
from src.schemas.schemas import SOrderResponse, SKpiReport
from src.models.models import Order, OrderNotIssuableError
from src.reports import get_kpi
from src.importers.import_csv_file import import_file
router = APIRouter(prefix="/order")


#ВЫВОД ОТЧЕТОВ
@router.get("/KPI", response_model=SKpiReport)
def get_kpi_report():
    con = get_connection()
    kpi = get_kpi(con)
    close_connection(con)
    return kpi


#ВЫВОД ЛОГОВ
@router.get("/logs")
def get_log():
    con = get_connection()
    log = con.cursor().execute("""SELECT *
                                FROM operation_log""").fetchall()
    close_connection(con)
    return {"Количество операций": len(log),
            "Операции":log}


#ПРОСМОТР ВСЕХ ЗАКАЗОВ
@router.get("")
def get_orders():
    con = get_connection()
    data_orders = con.cursor().execute("""SELECT *
                                        FROM orders""").fetchall()
    close_connection(con)
    return {"Заказов": len(data_orders), "data": data_orders}


#ПОСМОТРЕТЬ ЗАКАЗ ПО ID
@router.get("/{id}", response_model=SOrderResponse)
def get_one_orders(id:int):
    con = get_connection()
    try:
        orders = Order.find_by_id(con, id)
        if orders:
            return orders
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ №{id} не найден")
    finally:
        close_connection(con)


#ВЫДАЧА ЗАКАЗА
@router.patch("/{order_id}/issue", status_code=status.HTTP_200_OK)
def issue_order(order_id:int):
    con = get_connection()
    try:
        orders = Order.find_by_id(con, order_id)
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ №{order_id} не найден")
        orders.issue(emp_id=1)
        return {"status": orders.status, "message": f"Заказ №{order_id} выдан"}

    except OrderNotIssuableError:
            raise HTTPException(status_code=status.HTTP_200_OK, detail=f"Заказ уже выдан!")
    finally:
        close_connection(con)


#ОТМЕНА ЗАКАЗА
@router.patch("/{orders_id}/cancel")
def cancel_order(orders_id:int):
    con = get_connection()
    try:
        orders = Order.find_by_id(con, orders_id)
        if orders:
            orders.cancel(emp_id=1)
            return {"status": orders.status, "message": f"Заказ №{orders_id} отменён"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ №{orders_id} не найден")

    except OrderNotIssuableError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Заказ имеет статус '{orders.status}', отмена невозможна!")
    finally:
        close_connection(con)


#ВОЗВРАТ ЗАКАЗА
@router.patch("/{or_id}/refund")
def refund_order(or_id:int):
    con = get_connection()
    try:
        orders = Order.find_by_id(con, or_id)
        if orders:
            orders.vosvrat(emp_id=1)
            return {"status": orders.status, "message": f"Заказ №{or_id} возвращен"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ №{or_id} не найден")

    except OrderNotIssuableError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ имеет статус '{orders.status}'")
    finally:
        close_connection(con)

#ИМПОРТ CSV ФАЙЛОВ
@router.post("/file_csv")
def import_files():
    con = get_connection()
    import_file(con, 'data/orders_file.csv')
    close_connection(con)
    return {"Успешно!"}

