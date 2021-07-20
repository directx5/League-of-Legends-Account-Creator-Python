from requests import post

from exceptions import OutOfBalance


class TwoCaptcha:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def balance(self):
        return float(post('https://2captcha.com/res.php', {'key': self.api_key, 'action': 'getbalance'}).text)

    def solve(self):
        if self.balance() > 0:
            body = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'sitekey': 'a010c060-9eb5-498c-a7b9-9204c881f9dc',
                'pageurl': 'https://signup.tr.leagueoflegends.com/tr/signup/index',
                'soft_id': 2622,
            }
            try:
                captcha_id = post('https://2captcha.com/in.php', body).text.split('|')[1]
            except IndexError:
                return None

            body = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'action': 'get',
                'id': captcha_id,
                'soft_id': 2622,
            }
            token = post('https://2captcha.com/res.php', body).text

            while token == 'CAPCHA_NOT_READY':
                token = post('https://2captcha.com/res.php', body, timeout=5).text

            return token if (r := token.split('|')[1]) is None else r
        else:
            raise OutOfBalance(self.balance())
