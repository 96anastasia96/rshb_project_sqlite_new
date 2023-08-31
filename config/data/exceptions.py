class CustomException(Exception):
    pass


class NoCreditException(CustomException):
    '''Кредит отсутствует'''
    pass


class NotEnoughFundsException(CustomException):
    '''Недостаточно средств для возврата кредита'''
    pass