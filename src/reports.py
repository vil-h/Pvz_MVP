def get_kpi(con):
    cur = con.cursor()

    average_time_of_issue = cur.execute("""SELECT AVG(julianday(issued_at) - julianday(arrived_at))
                                        FROM orders
                                        WHERE issued_at IS NOT NULL""").fetchone()
    avg_time = average_time_of_issue[0] if average_time_of_issue and average_time_of_issue[0] is not None else 0

    issued_on_the_day_of_admission = cur.execute("""SELECT COUNT(order_id)
                                                    FROM orders
                                                    WHERE issued_at = arrived_at""").fetchone()

    same_day = issued_on_the_day_of_admission[0] if issued_on_the_day_of_admission else 0

    overdue_orders = cur.execute("""SELECT COUNT(status)
                                    FROM orders
                                    WHERE status = 'на складе' AND julianday('now') - julianday(arrived_at) > 7""").fetchone()

    overdue = overdue_orders[0] if overdue_orders else 0

    total_orders_processed = cur.execute("""SELECT COUNT(status)
                                            FROM orders
                                            WHERE status IN ('выдан', 'возврат', 'отменён')""").fetchone()
    processed = total_orders_processed[0] if total_orders_processed else 0

    kpi = {
        "avg_issue_time": round(avg_time, 2),
        "issued_same_day": same_day,
        "overdue_orders": overdue,
        "total_processed": processed
    }
    return kpi