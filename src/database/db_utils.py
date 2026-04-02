import sqlite3
def get_connection():
    con = sqlite3.connect("../data/database.db")
    db_init(con)
    return con

def db_init(con):
    # ТАБЛИЦА КЛИЕНТОВ
    con.execute("CREATE TABLE IF NOT EXISTS client (client_id INTEGER PRIMARY KEY, full_name VARCHAR)")
    con.execute("INSERT OR IGNORE INTO client (client_id, full_name) VALUES(1, 'Anton Smirnov')")
    con.execute("INSERT OR IGNORE INTO client (client_id, full_name) VALUES(2, 'PETR MILENOV')")

    # ТАБЛИЦА РАБОТНИКОВ
    con.execute("""
            CREATE TABLE IF NOT EXISTS employees(
            emp_id INTEGER PRIMARY KEY,
            first_name VARCHAR,
            last_name VARCHAR)""")

    con.execute("""INSERT OR IGNORE INTO employees(
                emp_id,
                first_name,
                last_name)
                VALUES(
                1,
                'VILDAN',
                'MUKAEV')""")

    # ТАБЛИЦА ТОВАРОВ
    con.execute("""CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY,
                client_id INTEGER,
                status VARCHAR,
                arrived_at TEXT,
                FOREIGN KEY (client_id) REFERENCES client(client_id))""")
    con.execute("""INSERT OR IGNORE INTO orders(
                order_id,
                client_id,
                status,
                arrived_at)
                VALUES(
                1,
                1,
                'выдан',
                '2026-03-30')""")

    # ТАБЛИЦА ЛОГОВ
    con.execute("""CREATE TABLE IF NOT EXISTS operation_log(
                    log_id INTEGER PRIMARY KEY,
                    order_id INTEGER,
                    emp_id INTEGER,
                    action TEXT,
                    time TEXT,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id) )""")

    con.execute("""INSERT OR IGNORE INTO operation_log(
                    log_id,
                    order_id,
                    emp_id,
                    action,
                    time)
                    VALUES(
                    1,
                    1,
                    1,
                    'Выдан',
                    '2026-03-30')""")

    con.commit()

def close_connection(con):
    con.close()
