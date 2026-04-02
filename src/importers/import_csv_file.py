import csv

def import_file(db, filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        cur = db.cursor()
        for row in reader:

            res = cur.execute("""SELECT client_id
                                    FROM client
                                    WHERE full_name = ?""", (row['full_name'],))
            res = res.fetchone()
            if res:
                client_id = res[0]
            else:

                cur.execute("""INSERT INTO client(
                                    full_name)
                                    VALUES(
                                    ?)""", (row['full_name'],))
                client_id = cur.lastrowid

            cur.execute("""INSERT OR IGNORE INTO orders(
                                order_id, 
                                client_id, 
                                status, 
                                arrived_at)
                                VALUES(
                                ?,
                                ?,
                                ?,
                                ?)""", (int(row['order_id']), client_id, row['status'], row['arrived_at']))
            db.commit()
