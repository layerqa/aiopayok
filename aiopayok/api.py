from .base import BaseClient
from .const import HTTPMethods

from .models.balance import Balance


class Aiopayok(BaseClient):
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
        api_key: str
    ) -> None:
        super().__init__()
        '''
        Init Payok API client

            :param api_id: Your API Key ID
            :param api_key: Your API Key
        '''
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

        data = await self._make_request(method, url, data=data)
        return Balance(**data)
        
