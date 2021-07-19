from json import dumps
from string import ascii_letters, digits
from random import choices

from captcha import TwoCaptcha

from requests import post


class Creator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'
        self.captcha = TwoCaptcha(self.api_key)

    def create(self):
        def data(length: int):
            return ''.join(choices(ascii_letters + digits, k=length))

        if self.captcha.balance() <= 0:
            raise ValueError(f'Not enough balance! Balance: {self.captcha.balance()}. Balance must be greater than 0.')

        request_body = {
            'username': (username := data(16)),
            'password': (password := data(16)),
            'confirm_password': password,
            'date_of_birth': '2000-01-01',
            'email': (email := f'{username}@direct.com'),
            'tou_agree': True,
            'newsletter': False,
            'region': 'TR1',
            'campaign': 'league_of_legends',
            'locale': 'tr',
            'token': f'hcaptcha {self.captcha.solve()}',
        }
        response = post(url=self.api_url, data=dumps(request_body), headers={'Content-Type': 'application/json'},
                        timeout=10)

        return response.json(), dumps({'username': username, 'password': password, 'email': email})


if __name__ == '__main__':
    creator = Creator('API_KEY')
    print(creator.create())
