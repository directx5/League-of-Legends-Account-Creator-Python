from requests import post


class TwoCaptcha:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def balance(self):
        return float(post('https://2captcha.com/res.php', data={'key': self.api_key, 'action': 'getbalance'}).text)

    def solve(self):
        if self.balance() > 0:
            payload = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'sitekey': 'a010c060-9eb5-498c-a7b9-9204c881f9dc',
                'pageurl': 'https://signup.tr.leagueoflegends.com/tr/signup/index',
                'soft_id': 2622
            }
            try:
                captcha_id = post('https://2captcha.com/in.php', data=payload).text.split('|')[1]
            except IndexError:
                return None

            payload = {
                'key': self.api_key,
                'method': 'hcaptcha',
                'action': 'get',
                'id': captcha_id,
                'soft_id': 2622,
            }
            token = post('https://2captcha.com/res.php', data=payload).text
            while token == 'CAPCHA_NOT_READY':
                token = post('https://2captcha.com/res.php', data=payload, timeout=(.5, 5)).text

            return token.split('|')[1]
        else:
            return None
