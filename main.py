from json import dumps
from string import ascii_letters, digits
from random import choices

from captcha import solve

from requests import post

api_key = 'API_KEY'
api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'

balance = float(post('https://2captcha.com/res.php', {'key': api_key, 'action': 'getbalance'}).text)

if balance <= 0:
    raise ValueError(f'Not enough balance! Balance: {balance}. Balance must be greater than 0.')


def generate(length: int):
    return ''.join(choices(ascii_letters + digits, k=length))


request_body = {
        'username': (username := generate(14)),
        'password': (password := generate(14)),
        'confirm_password': password,
        'date_of_birth': '2000-01-01',
        'email': (email := f'{username}@direct.com'),
        'tou_agree': True,
        'newsletter': False,
        'region': 'TR1',
        'campaign': 'league_of_legends',
        'locale': 'tr',
        'token': f'hcaptcha {solve(api_key)}',
    }
response = post(url=api_url, data=dumps(request_body), headers={'Content-Type': 'application/json'}, timeout=10)

print(response.json())
print(dumps({'username': username, 'password': password, 'email': email}))
