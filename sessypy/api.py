from aiohttp import BasicAuth
import aiohttp
from .const import SessyApiCommand


class SessyApi:
    def __init__(self, host, username, password):
        self.host = host
        
        self.session = aiohttp.ClientSession(
            auth=BasicAuth(username, password)
        )
    
    async def get(self, command):
        url = self._command_url(command)
        response = await self.session.get(url)
        return await response.json()
    
    async def post(self, command: SessyApiCommand, data: dict):
        url = self._command_url(command)
        response = await self.session.post(url, json = data)
        return await response.json()
        
    def _command_url(self, command: SessyApiCommand):
        return f"http://{self.host}/{command.value}"
    
    async def close(self):
        await self.session.close()