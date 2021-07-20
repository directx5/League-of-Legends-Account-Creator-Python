import asyncio
from json import dumps
from os import path
from random import choices
from string import ascii_letters, digits

from requests import post

from captcha import TwoCaptcha
from exceptions import OutOfBalance


class Creator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'
        self.captcha = TwoCaptcha(self.api_key)

    async def create(self):
        def data(length: int):
            return ''.join(choices(ascii_letters + digits, k=length))

        if await self.captcha.balance() <= 0:
            raise OutOfBalance(await self.captcha.balance())

        token = await self.captcha.solve()
        if token:
            body = {
                'username': (username := data(16)),
                'password': (password := data(16)),
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
            response = post(self.api_url, dumps(body), headers={'Content-Type': 'application/json'})

            print(response.json())
            print(dumps({'username': username, 'password': password, 'email': email}))

            combo = f'{username}:{password}'
            if path.exists('last.txt'):
                with open('last.txt', 'a', encoding='UTF-8') as file:
                    file.write(f'{combo}\n')
            else:
                with open('last.txt', 'w', encoding='UTF-8') as file:
                    file.write(f'{combo}\n')


if __name__ == '__main__':
    creator = Creator('API_KEY')
    asyncio.get_event_loop().run_until_complete(creator.create())
