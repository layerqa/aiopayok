from .base import BaseClient
from .const import HTTPMethods

from .models.balance import Balance
from .models.transaction import Transaction, Transactions

from typing import Optional, Union


class Aiopayok(BaseClient):
    '''
    Payok API client.

        Consists of API methods only.
        All other methods are hidden in the BaseClient.
    '''

    API_HOST = 'https://payok.io'
    API_DOCS = 'https://payok.io/cabinet/documentation/doc_main.php'

    def __init__(self, api_id: int, api_key: str) -> None:
        '''
        Init Payok API client

            :param api_id: Your API Key ID
            :param api_key: Your API Key
        '''
        super().__init__()
        self.__api_id = api_id
        self.__api_key = api_key
    
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
        shop: int,
        payment: Optional[int] = None,
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
        data = {'API_ID': self.__api_id, 'API_KEY': self.__api_key, 'shop': shop}
        if payment:
            data['payment'] = payment
        if offset:
            data['offset'] = offset
        
        response = await self._make_request(method, url, data=data)
        if payment:
            return Transaction(**response['1'])
        if payment is None:
            transactions = []
            for i in list(response.keys())[1:]:
                transactions.append(Transaction(**response[i]))
            return Transactions(transactions=transactions)


        
