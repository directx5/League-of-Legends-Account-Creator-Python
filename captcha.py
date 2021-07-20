from asyncio import sleep

from aiohttp import ClientSession

from exceptions import OutOfBalance


class TwoCaptcha:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def balance(self):
        async with ClientSession() as s:
            async with s.post('https://2captcha.com/res.php', data={'key': self.api_key, 'action': 'getbalance'}) as r:
                return float((await r.read()).decode('UTF-8'))

    async def solve(self):
        if await self.balance() > 0:
            payload = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'sitekey': 'a010c060-9eb5-498c-a7b9-9204c881f9dc',
                'pageurl': 'https://signup.tr.leagueoflegends.com/tr/signup/index',
                'soft_id': 2622
            }
            async with ClientSession() as s:
                async with s.post('http://2captcha.com/in.php', data=payload) as r:
                    try:
                        captcha_id = (await r.read()).decode('UTF-8').split('|')[1]
                    except IndexError:
                        return None

            payload = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'action': 'get',
                'id': captcha_id,
                'soft_id': 2622,
            }
            async with ClientSession() as s:
                async with s.post('http://2captcha.com/res.php', data=payload) as r:
                    token = (await r.read()).decode('UTF-8')

                while token == 'CAPCHA_NOT_READY':
                    await sleep(5)
                    async with s.post('http://2captcha.com/res.php', data=payload) as r:
                        token = (await r.read()).decode('UTF-8')

            return token.split('|')[1]
        else:
            raise OutOfBalance
