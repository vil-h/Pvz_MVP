from datetime import datetime
class OrderNotIssuableError(Exception): pass
class Order:
    def __init__(self, db, order_id, client_id, status, arrived_at,issued_at = None):
        self.db = db
        self.order_id = order_id
        self.client_id = client_id
        self.status = status
        self.arrived_at = arrived_at
        self.issued_at = issued_at

    @classmethod
    def find_by_id(cls, db, order_id):
        a = db.cursor().execute("""SELECT order_id, client_id, status, arrived_at, issued_at
                                FROM orders
                                WHERE order_id = ?""", (order_id,)).fetchone()

        if a is not None:
            order_id, client_id, status, arrived_at, issued_at = a
            return cls(db, order_id, client_id, status, arrived_at,issued_at)
        else:
            return None

    def issue(self, emp_id):

        if self.status.lower() == 'на складе'.lower():
            self.status = 'выдан'
            self.issued_at = datetime.now().strftime('%Y-%m-%d')
            self.db.cursor().execute("""UPDATE orders
                                SET status = ?, issued_at = ?
                                WHERE order_id = ?""", ('выдан', self.issued_at, self.order_id))
            self.db.cursor().execute("""INSERT INTO operation_log(
                                        order_id,
                                        emp_id,
                                        action,
                                        time)
                                        VALUES(
                                        ?,
                                        ?,
                                        ?,
                                        datetime('now'))""", (self.order_id, emp_id, 'выдан'))
            self.db.commit()
        else:
            raise OrderNotIssuableError(f"товар {self.order_id} имеет статус: {self.status}")


    def cancel(self, emp_id):
        if self.status.lower() == "на складе":
            self.status = "отменен"
            self.db.cursor().execute("""UPDATE orders
                                        SET status = ?
                                        WHERE order_id = ?""", ('отменен', self.order_id))
            self.db.cursor().execute("""INSERT INTO operation_log(
                                        order_id,
                                        emp_id,
                                        action,
                                        time)
                                        VALUES(
                                        ?,
                                        ?,
                                        ?,
                                        datetime('now'))""", (self.order_id, emp_id, 'отменен'))
            self.db.commit()
        else:
            raise OrderNotIssuableError(f"товар {self.order_id} имеет статус: {self.status}")


    def vosvrat(self, emp_id):
        if self.status.lower() == 'выдан':
            self.status = 'возврат'
            self.db.cursor().execute("""UPDATE orders
                                                    SET status = ?
                                                    WHERE order_id = ?""", ('возврат', self.order_id))
            self.db.cursor().execute("""INSERT INTO operation_log(
                                                    order_id,
                                                    emp_id,
                                                    action,
                                                    time)
                                                    VALUES(
                                                    ?,
                                                    ?,
                                                    ?,
                                                    datetime('now'))""", (self.order_id, emp_id, 'возврат'))
            self.db.commit()
        else:
            raise OrderNotIssuableError(f"товар {self.order_id} имеет статус: {self.status}")