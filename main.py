from json import dumps
from os import path
from random import choices
from string import ascii_letters, digits
from threading import Thread

from requests import post

from captcha import TwoCaptcha


class Creator:
    def __init__(self, api_key: str):
        self.api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'
        self.captcha = TwoCaptcha(api_key)

    def create(self):
        def data(length: int):
            return ''.join(choices(ascii_letters, k=length // 2)) + ''.join(choices(digits, k=length // 2))

        token = self.captcha.solve()
        if token:
            body = {
                'username': (username := data(24)),
                'password': (password := data(24)),
                'confirm_password': password,
                'date_of_birth': '2000-01-01',
                'email': (email := f'{username[::-1]}@{username[3:int(len(username) // 2)]}.com'),
                'tou_agree': True,
                'newsletter': False,
                'region': 'TR1',
                'campaign': 'league_of_legends',
                'locale': 'tr',
                'token': f'hcaptcha {token}',
            }
            response = post(self.api_url, dumps(body), headers={'Content-Type': 'application/json'}, timeout=(.5, 5))

            if 'account' in (rj := response.json()).keys():
                print(dumps(rj))
                print(dumps({'username': username, 'password': password, 'email': email}))

                mode = 'a' if path.exists('accounts.txt') else 'w'
                with open('accounts.txt', mode, encoding='UTF-8') as file:
                    file.write(f'{username}:{password}\n')
        else:
            print(f'Passing, not enough balance! Your balance: {self.captcha.balance()}')

    def run(self, count: int = 1):
        if count <= 0:
            raise ValueError('Count must be greater than 0.')
        elif count == 1:
            self.create()
        else:
            threads = [Thread(target=self.create, daemon=True) for _ in range(count)]
            for th in threads:
                th.start()
            for th in threads:
                th.join()


if __name__ == '__main__':
    captcha_api_key = 'API_KEY'
    Creator(captcha_api_key).run()
