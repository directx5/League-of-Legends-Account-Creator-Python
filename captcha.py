from twocaptcha import api, TwoCaptcha as Captcha


class TwoCaptcha:
    def __init__(self, api_key: str):
        self.api_key = api_key
        config = {
            'server': '2captcha.com',
            'apiKey': api_key,
            'defaultTimeout': 60,
            'pollingInterval': 5,
        }
        self.__solver = Captcha(**config)

    def balance(self):
        return self.__solver.balance()

    def solve(self):
        try:
            result = self.__solver.hcaptcha('a010c060-9eb5-498c-a7b9-9204c881f9dc',
                                            'https://signup.tr.leagueoflegends.com/tr/signup/index')
            return result['code']
        except api.ApiException:
            return None
