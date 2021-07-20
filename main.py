from asyncio import get_event_loop
from json import dumps
from os import path
from random import choices
from string import ascii_letters, digits

from aiohttp import ClientSession

from captcha import TwoCaptcha
from exceptions import OutOfBalance


class Creator:
    def __init__(self, api_key: str):
        self.api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'
        self.captcha = TwoCaptcha(api_key)

    async def create(self):
        def data(length: int):
            result = ''.join(choices(ascii_letters + digits, k=length))
            while not any(x.isdigit() for x in result) or any(not x.isdigit() for x in result):
                result = data(length)
            return result

        if await self.captcha.balance() <= 0:
            raise OutOfBalance(await self.captcha.balance())

        token = await self.captcha.solve()
        if token:
            body = {
                'username': (username := data(24)),
                'password': (password := data(24)),
                'confirm_password': password,
                'date_of_birth': '2000-01-01',
                'email': (email := f'{username[::-1]}@randwoboo.com'),
                'tou_agree': True,
                'newsletter': False,
                'region': 'TR1',
                'campaign': 'league_of_legends',
                'locale': 'tr',
                'token': f'hcaptcha {token}',
            }
            async with ClientSession() as s:
                async with s.post(self.api_url, data=dumps(body), headers={'Content-Type': 'application/json'}) as r:
                    response = await r.json()

            print(dumps(response))
            print(dumps({'username': username, 'password': password, 'email': email}))

            combo = f'{username}:{password}'
            if path.exists('accounts.txt'):
                with open('accounts.txt', 'a', encoding='UTF-8') as file:
                    file.write(f'{combo}\n')
            else:
                with open('accounts.txt', 'w', encoding='UTF-8') as file:
                    file.write(f'{combo}\n')


if __name__ == '__main__':
    creator = Creator('API_KEY')
    get_event_loop().run_until_complete(creator.create())
