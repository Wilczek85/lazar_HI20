import aiohttp

class LazarAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None

    async def async_login(self):
        self.session = aiohttp.ClientSession()
        async with self.session.post(
            "https://hkslazar.net/sollogin",
            data={"login": self.username, "password": self.password},
            timeout=10
        ) as resp:
            if resp.status != 200:
                raise RuntimeError("Login failed")

    async def async_fetch(self):
        async with self.session.get(
            "https://hkslazar.net/oemSerwis?what=bcst",
            timeout=10
        ) as resp:
            return await resp.json()

    async def async_close(self):
        if self.session:
            await self.session.close()
