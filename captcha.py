from time import sleep

from requests import post


def solve(api_key: str):
    balance = float(post('https://2captcha.com/res.php', {'key': api_key, 'action': 'getbalance'}).text)
    if balance > 0:
        body = {
            'key': api_key,
            'method': 'hcaptcha',
            'sitekey': 'a010c060-9eb5-498c-a7b9-9204c881f9dc',
            'pageurl': 'https://signup.tr.leagueoflegends.com/tr/signup/index',
            'soft_id': 2622,
        }

        captcha_id = post('https://2captcha.com/in.php', body).text.split('|')[1]

        body = {
            'key': api_key,
            'method': 'hcaptcha',
            'action': 'get',
            'id': captcha_id,
            'soft_id': 2622,
        }

        token = post('https://2captcha.com/res.php', body, timeout=5).text

        while token == 'CAPCHA_NOT_READY':
            sleep(5)
            token = post('https://2captcha.com/res.php', body, timeout=5).text

        return token if (r := token.split('|')[1]) is None else r
    else:
        raise ValueError(f'Balance ran out!')
