from pydantic import BaseModel

from typing import List


class Transaction(BaseModel):
    '''Payok API transaction model'''

    transaction: int
    email: str
    amount: float
    currency: str
    currency_amount: float
    comission_percent: float
    comission_fixed: float
    amount_profit: float
    method: str
    payment_id: int
    description: str
    date: str
    pay_date: str
    transaction_status: int
    custom_fields: str
    webhook_status: int
    webhook_amount: int

class Transactions(BaseModel):
    '''Payok API transactions model'''

    transactions: List[Transaction]