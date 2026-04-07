from pydantic import BaseModel

class SOrderResponse(BaseModel):
    order_id:int
    client_id:int
    status:str
    arrived_at: str
    issued_at: str | None

class SKpiReport(BaseModel):
    avg_issue_time: float
    issued_same_day: int
    overdue_orders: int
    total_processed: int