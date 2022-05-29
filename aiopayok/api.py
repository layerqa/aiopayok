from .base import BaseClient
from .const import HTTPMethods
import hashlib
from .models.balance import Balance
from .models.transaction import Transaction, Transactions

from typing import Optional, Union


class Payok(BaseClient):
    '''
    Payok API client.

        Consists of API methods only.
        All other methods are hidden in the BaseClient.
    '''

    API_HOST = 'https://payok.io'
    API_DOCS = 'https://payok.io/cabinet/documentation/doc_main.php'

    def __init__(
        self,
        api_id: int,
        api_key: str,
        secret_key: Optional[str] = None,
        shop: Optional[int] = None,
    ) -> None:
        '''
        Init Payok API client

            :param api_id: Your API Key ID
            :param api_key: Your API Key
        '''
        super().__init__()
        self.__api_id = api_id
        self.__api_key = api_key
        self._secret_key = secret_key
        self._shop = shop

    async def get_balance(self) -> Balance:
        '''
        Get balance and ref balance

            Docs: https://payok.io/cabinet/documentation/doc_api_balance
        '''
        method = HTTPMethods.POST
        url = f'{self.API_HOST}/api/balance'
        data = {'API_ID': self.__api_id, 'API_KEY': self.__api_key}

        response = await self._make_request(method, url, data=data)
        return Balance(**response)

    async def get_transactions(
        self,
        shop: Optional[int] = None,
        payment: Optional[Union[int, str]] = None,
        offset: Optional[int] = None
    ) -> Union[Transaction, Transactions]:
        '''
        Get transactions

            :param shop: Store ID
            :param payment: Payment ID
            :param offset: Indent, skip the specified number of lines

            Docs: https://payok.io/cabinet/documentation/doc_api_transaction
        '''
        method = HTTPMethods.POST
        url = f'{self.API_HOST}/api/transaction'
        data = {
            'API_ID': self.__api_id,
            'API_KEY': self.__api_key,
            'shop': shop or self._shop
        }
        if payment:
            data['payment'] = payment
        if offset:
            data['offset'] = offset

        response = await self._make_request(method, url, data=data)

        if response.pop("status") == "error":
            raise Exception(response)

        if payment:
            return Transaction(**response['1'])

        transactions = []
        for i in list(response.keys())[1:]:
            transactions.append(Transaction(**response[i]))

        return Transactions(**transactions)

    async def create_pay(
        self,
        payment: str,
        amount: float,
        currency: Optional[str] = "RUB",
        desc: Optional[str] = None,
        email: Optional[str] = None,
        success_url: Optional[str] = None,
        method: Optional[str] = None,
        lang: Optional[str] = None,
        custom: Optional[str] = None
    ) -> str:
        '''
        Create payform url

            :param payment: Order number, unique in your system, up to 16 characters. (a-z0-9-_)
            :param amount : Order amount.
            :param currency : ISO 4217 currency. Default is "RUB".
            :param desc : Product name or description.
            :param email : Email Buyer mail. Defaults to None.
            :param success_url: Link to redirect after payment.
            :param method: Payment method
            :param lang: Interface language. RU or EN
            :param custom: Parameter that you want to pass in the notification.

            Docs: https://payok.io/cabinet/documentation/doc_payform.php
        '''
        method = HTTPMethods.GET
        url = f"{self.API_HOST}/pay?amount={amount}&payment={payment}&shop={self._shop}&desc={desc}&email={email}&success_url=&method={method}&lang={lang}&custom={custom}"
        if not self._secret_key:
            raise Exception("secret key is empty")
        data = [
            amount,
            payment,
            self._shop,
            currency,
            desc,
            self._secret_key,
        ]
        params = "|".join(map(str, data))
        sign = hashlib.md5(params.encode("utf-8")).hexdigest()
        r = await self._make_request("GET", url := f"{url}&sign={sign}")
        if "pay_error_text" in r:
            raise Exception("Invalid payform sign")
        return url
