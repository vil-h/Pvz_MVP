from db_utils import get_connection, close_connection
from models import Order
from import_csv_file import import_file

con = get_connection()

C:\Users\THUNDEROBOT\PycharmProjects\pythonProjectAIR2
print("Для работы укажите свой Логин(ID):")
EMP_ID = int(input())
name = con.cursor().execute("""SELECT last_name, first_name
                                    FROM employees
                                    WHERE emp_id = ?""", (EMP_ID,)).fetchall()
if name:
    print(f"Добрый день, {name[0][0]} {name[0][1]}")
else:
    raise IndexError(f"Не существует сотрудника с ID {EMP_ID}")


print("Добро пожаловать в систему ПВЗ!")
while True:
    print("""
1.  Показать все заказы
2.  Найти заказ по номеру
3.  Выдать заказ
4.  Отменить заказ
5.  Оформить возврат
6.  Показать журнал операций
7.  Импортировать заказы из CSV
8.  Показать отчёты
9.  Выйти""")
    a = int(input())
    if a == 1:
        data_orders = con.cursor().execute("""SELECT *
                                            FROM orders""").fetchall()
        print(f"В система {len(data_orders)} заказов:")
        for i in data_orders:
            print(f"Заказ № {i[0]}, Клиент: {i[1]}, Статус: {i[2]}, Дата: {i[3]}")


    if a == 2:
        id = int(input("Введите ID заказа: "))
        d = Order.find_by_id(con, id)
        if d:
            print(f"""Данные по заказу {id}: 
                    ID Клиента:{d.client_id}
                    Статус заказа: {d.status}
                    Дата заказа: {d.arrived_at}""")
        else:
            print(f"Товар с ID {id} не найден")


    if a == 3:
        order_id = int(input("Введите ID заказа: "))
        order = Order.find_by_id(con, order_id)
        if order:
            order.issue(EMP_ID)
            print(f"Статус изменён на: '{order.status}'")
        else:
            print(f"Заказ {order_id} не найден")

    if a == 4:
        print("Введите ID заказа: ")
        ord_id = int(input())
        ordid = Order.find_by_id(con, ord_id)
        ordid.cancel(EMP_ID)
        print(f"Статус изменен на: '{ordid.status}'")

    if a == 5:
        print("Введите ID заказа: ")
        ord_id = int(input())
        ordid = Order.find_by_id(con, ord_id)
        ordid.vosvrat(EMP_ID)
        print(f"Статус изменен на: '{ordid.status}'")

    if a == 6:
        data_log = con.cursor().execute("""SELECT *
                                                    FROM operation_log""").fetchall()
        print(f"В система {len(data_log)} операций:")
        for i in data_log:
            print(i)

    if a == 9:
        print("Хорошего дня")
        break

close_connection(con)