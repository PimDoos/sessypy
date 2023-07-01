from aiohttp import BasicAuth, ClientConnectionError, ClientResponseError, ContentTypeError
import aiohttp
from .const import SessyApiCommand
from .util import SessyConnectionException, SessyLoginException, SessyNotSupportedException


class SessyApi:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        
        self.session = aiohttp.ClientSession(
            auth=BasicAuth(username, password),
            raise_for_status = True
        )
    
    async def get(self, command):
        return await self.request("GET", command)
    async def post(self, command: SessyApiCommand, data: dict = None):
        return await self.request("POST", command, data)
    
    async def request(self, method: str, command: SessyApiCommand, data = None):
        try:
            url = self._command_url(command)
            response = await self.session.request(method, url, json = data)
            return await response.json()
        except ClientConnectionError:
            raise SessyConnectionException
        except ContentTypeError:
            raise SessyNotSupportedException
        except ClientResponseError as e:
            if e.status == 401:
                raise SessyLoginException
            else:
                raise SessyNotSupportedException
        
        
    def _command_url(self, command: SessyApiCommand):
        return f"http://{self.host}/{command.value}"
    
    async def close(self):
        await self.session.close()
    
