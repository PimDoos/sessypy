import logging
from aiohttp import BasicAuth, ClientConnectionError, ClientResponseError, ContentTypeError
import aiohttp
from .const import SessyApiCommand
from .util import SessyConnectionException, SessyLoginException, SessyNotSupportedException

_LOGGER = logging.getLogger(__name__)

class SessyApi:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username

        self.session = aiohttp.ClientSession(
            auth=BasicAuth(username, password),
            raise_for_status = True,
            timeout = aiohttp.ClientTimeout(total=5)
        )

    async def get(self, command):
        return await self.request("GET", command)
    async def post(self, command: SessyApiCommand, data: dict = None):
        return await self.request("POST", command, data)

    async def request(self, method: str, command: SessyApiCommand, data = None):
        try:
            url = self._command_url(command)
            _LOGGER.debug(f"Sending {method} request to {url} with data {data}")
            response = await self.session.request(method, url, json = data)
            return await response.json()
        
        except ClientConnectionError as e:
            _LOGGER.debug(f"{method} request to {url} raised a connection error: {e}")
            raise SessyConnectionException from e
    
        except TimeoutError as e:
            _LOGGER.debug(f"{method} request to {url} timed out: {e}")
            raise SessyConnectionException from e
        
        except ContentTypeError as e:
            _LOGGER.debug(f"{method} request to {url} returned content of an unexpected type: {e.message}")
            raise SessyNotSupportedException from e
        
        except ClientResponseError as e:
            _LOGGER.debug(f"{method} request to {url} returned an error response code: {e.status} {e.message}")
            if e.status == 401:
                raise SessyLoginException from e
            else:
                raise SessyNotSupportedException from e

    def _command_url(self, command: SessyApiCommand):
        return f"http://{self.host}/{command.value}"

    async def close(self):
        await self.session.close()
