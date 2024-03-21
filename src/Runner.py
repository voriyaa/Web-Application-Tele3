from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hashlib import sha256
from BaseUser import Base
from AdminAccount import AdminAccount, Tariff
from UserAccount import UserAccount
from Constants import Constant


def sha256_str(item):
    return sha256(str(item).encode()).hexdigest()


# DATABASE_URL = 'postgresql://postgres:123@192.168.0.105:5432/test'
db_file = 'example.db'

DATABASE_URL = f'sqlite:///{db_file}'

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)
s = session()


class App:

    @staticmethod
    def run():
        print(Constant.HI_TO_USER)
        variant = App.get_variant()

        if variant == 1:
            App.admin_workflow()
        else:
            App.user_workflow()

    @staticmethod
    def get_variant():
        variant = int(input(Constant.CHOOSE_STATUS))
        while variant not in [1, 2]:
            variant = int(input(Constant.CHOOSE_OPTION_1))
        return variant

    @staticmethod
    def view_tariffs():
        list_of_tariff = s.query(Tariff)

        print(Constant.LIST_SERVICES)
        for elem in list_of_tariff:
            print(
                f"{elem.id}: {elem.get_gb()}ГБ. | {elem.get_minutes()}мин. |"
                f" {elem.get_cost_one_gb()}руб/гб. "
                f"| {elem.get_cost_one_minute()}руб/гб. | {elem.get_price()}руб.")

    @staticmethod
    def admin_workflow():
        App.verify_secret_key()

        variant = App.choose_admin_option()
        if variant == 0:
            App.run()
            return
        elif variant == 1:
            admin = App.create_admin_account()
        else:
            admin = App.admin_login()

        admin.handle_admin_action()

    @staticmethod
    def choose_admin_option():
        variant = int(input(Constant.CHOOSE_OPTION_2))
        while variant not in [0, 1, 2]:
            variant = int(input(Constant.CHOOSE_CORRECT_OPTION))
        return variant

    @staticmethod
    def verify_secret_key():
        key = input(Constant.ENTER_SECRET_KEY)
        while sha256_str(key) != Constant.SECRET_KEY:
            key = input(Constant.WRONG_KEY)

    @staticmethod
    def create_admin_account():
        first_name = input(Constant.ENTER_NAME)
        last_name = input(Constant.ENTER_SURNAME)
        birth_date = input(Constant.ENTER_BIRTH_DATE)
        sex = input(Constant.ENTER_YOUR_SEX)
        passport_id = int(input(Constant.ENTER_PASSPORT_ID))
        phone_number = input(Constant.ENTER_PHONE_NUMBER)
        username = input(Constant.ENTER_USERNAME)
        password = input(Constant.ENTER_PASSWORD)

        admin = AdminAccount(first_name, last_name, birth_date, passport_id, sex,
                             username, password, phone_number)

        s.add(admin)
        s.commit()

        return admin

    @staticmethod
    def admin_login():
        username = input(Constant.ENTER_USERNAME)
        password = sha256_str(input(Constant.ENTER_PASSWORD))

        result = s.query(AdminAccount).filter(
            AdminAccount._AdminAccount__username == username and
            AdminAccount._AdminAccount__password == password).all()

        while len(result) == 0:
            print(Constant.INCORRECT_LOGIN_PASSWORD)
            username = input(Constant.ENTER_USERNAME)
            password = sha256_str(input(Constant.ENTER_PASSWORD))
            result = s.query(AdminAccount).filter(
                AdminAccount._AdminAccount__username == username and
                AdminAccount._AdminAccount__password == password).all()

        return result[0]

    @staticmethod
    def user_workflow():
        variant = App.choose_user_option()

        if variant == 0:
            App.run()
            return
        elif variant == 1:
            user = App.create_user_account()
        else:
            user = App.user_login()

        user.handle_user_actions()

    @staticmethod
    def choose_user_option():
        variant = int(input(Constant.CHOOSE_OPTION_2))
        while variant not in [0, 1, 2]:
            variant = int(input(Constant.CHOOSE_OPTION_1))
        return variant

    @staticmethod
    def create_user_account():
        first_name = input(Constant.ENTER_NAME)
        last_name = input(Constant.ENTER_SURNAME)
        birth_date = input(Constant.ENTER_BIRTH_DATE)
        sex = input(Constant.ENTER_YOUR_SEX)
        passport_id = int(input(Constant.ENTER_PASSPORT_ID))
        phone_number = input(Constant.ENTER_PHONE_NUMBER)
        username = input(Constant.ENTER_USERNAME)
        password = sha256_str(input(Constant.ENTER_PASSWORD))

        list_of_tariff = s.query(Tariff)
        App.display_tariffs(list_of_tariff)

        option = App.choose_tariff_option(list_of_tariff)

        user = UserAccount(first_name, last_name, birth_date, passport_id, sex,
                           username, password, phone_number,
                           list_of_tariff[option - 1])

        s.add(user)
        s.commit()

        return user

    @staticmethod
    def display_tariffs(tariffs):
        print(Constant.LIST_SERVICES)
        for i, elem in enumerate(tariffs):
            print(
                f"{i + 1}: {elem.get_gb()}ГБ. | {elem.get_minutes()}мин. |"
                f" {elem.get_cost_one_gb()}руб/гб. "
                f"| {elem.get_cost_one_minute()}руб/гб. | {elem.get_price()}руб.")

    @staticmethod
    def choose_tariff_option(tariffs):
        option = int(input(Constant.CHOOSE_OPTION_4))
        while not (
                (tariffs[0]).id <= option <= (tariffs[tariffs.count() - 1]).id):
            option = int(input(Constant.CHOOSE_CORRECT_OPTION_2))
        return option

    @staticmethod
    def user_login():
        username = input(Constant.ENTER_USERNAME)
        password = sha256_str(input(Constant.ENTER_PASSWORD))

        result = s.query(UserAccount).filter(
            UserAccount._UserAccount__username == username and
            UserAccount._UserAccount__password == password).all()

        while len(result) == 0:
            print(Constant.INCORRECT_LOGIN_PASSWORD)
            username = input(Constant.ENTER_USERNAME)
            password = sha256_str(input(Constant.ENTER_PASSWORD))
            result = s.query(UserAccount).filter(
                UserAccount._UserAccount__username == username and
                UserAccount._UserAccount__password == password).all()

        user = result[0]
        return user


App.run()
