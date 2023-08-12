from typing import Union, Optional

from pydantic import BaseModel


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
    method: Optional[str]
    payment_id: Union[int, str]
    description: str
    date: str
    pay_date: str
    transaction_status: int
    custom_fields: str
    webhook_status: int
    webhook_amount: int
