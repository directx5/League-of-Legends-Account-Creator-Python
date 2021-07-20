class OutOfBalance(Exception):
    def __init__(self, current_balance: float, message: str = 'Not enough balance!'):
        self.current_balance = current_balance
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} Your balance: {self.current_balance}'
