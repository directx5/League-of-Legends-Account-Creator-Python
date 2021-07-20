from json import dumps
from random import choices
from string import ascii_letters, digits
from threading import Thread

from requests import post

from captcha import TwoCaptcha
from exceptions import OutOfBalance


class Creator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'
        self.captcha = TwoCaptcha(self.api_key)

    def create(self):
        def data(length: int):
            return ''.join(choices(ascii_letters + digits, k=length))

        if self.captcha.balance() <= 0:
            raise OutOfBalance(self.captcha.balance())

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
            'token': f'hcaptcha {(self.captcha.solve())}',
        }
        response = post(self.api_url, dumps(body), headers={'Content-Type': 'application/json'})

        print(response.json())
        print(dumps({'username': username, 'password': password, 'email': email}))


if __name__ == '__main__':
    captcha_api_key = 'API_KEY'
    max_count = Creator(captcha_api_key).captcha.balance() // 0.00299
    threads = [Thread(target=Creator(captcha_api_key).create, daemon=True) for _ in range(int(max_count))]

    for th in threads:
        th.start()

    for th in threads:
        th.join()
