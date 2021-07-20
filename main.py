from json import dumps
from random import choices
from string import ascii_letters, digits
from threading import Thread

from requests import post

from captcha import TwoCaptcha


class Creator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'
        self.captcha = TwoCaptcha(self.api_key)

    def create(self):
        def data(length: int):
            return ''.join(choices(ascii_letters + digits, k=length))

        if self.captcha.balance() <= 0:
            raise ValueError(f'Not enough balance! Balance: {self.captcha.balance()}. Balance must be greater than 0.')

        body = {
            'username': (username := data(16)),
            'password': (password := data(16)),
            'confirm_password': password,
            'date_of_birth': '2000-01-01',
            'email': (email := f'{username}@randwoboo.com'),
            'tou_agree': True,
            'newsletter': False,
            'region': 'TR1',
            'campaign': 'league_of_legends',
            'locale': 'tr',
            'token': f'hcaptcha {(self.captcha.solve())}',
        }
        post(self.api_url, dumps(body))

        print(dumps({'username': username, 'password': password, 'email': email}))


if __name__ == '__main__':
    threads = [Thread(target=Creator('API_KEY').create, daemon=True) for _ in range(2)]

    for th in threads:
        th.start()

    for th in threads:
        th.join()
