from BaseUser import BaseUser, Column, String, Integer
from Tariff import Tariff
from hashlib import sha256


def sha256_str(item):
    return sha256(str(item).encode()).hexdigest()


class AdminAccount(BaseUser):

    id = Column(Integer, primary_key=True)

    def __init__(self, first_name, last_name, birth_date, passport_id, sex,
                 username: str, password: str, phone_number: str) -> None:
        super().__init__(first_name, last_name, birth_date, passport_id, sex)
        self.__username = username
        self.__password = password
        self.__phone_number = phone_number

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_phone_number(self) -> str:
        return self.__phone_number

    @staticmethod
    def create_tariff(cost_one_gb: int, cost_one_minute: int,
                      price: int, gb: int, minute: int) -> Tariff:
        return Tariff(cost_one_gb, cost_one_minute, price, gb, minute)

    @staticmethod
    def change_tariff(old_tariff: Tariff, cost_one_gb: int,
                      cost_one_minute: int, price: int, gb: int, minute: int) -> None:
        old_tariff.change_tariff(cost_one_gb, cost_one_minute, price, gb, minute)


    __tablename__ = 'admin_account'
    __username = Column(String(1000), unique=True)
    __password = Column(String(1000), unique=False)
    __phone_number = Column(String(1000), unique=True)

