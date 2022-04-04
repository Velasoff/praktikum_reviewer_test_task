# когда используется определенный модуль или элемент из библиотеки стоит подумать над использованием from ... import ...
import datetime as dt


# можно определять класс внутри другого класса, если используемый класс указывается только внутри конечного класса или
# дочерних классов от конечного
class Record:
    # вместо условия для установки текущей даты можно сразу дефолтным установить текущее, и при желании изменить
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # разделять строку можно для лучшей читаемости при нескольких задаваемых аргументов, но здесь нужно напрячься,
        # чтобы понять, гда применяется date
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    """
    Здесь интересный момент:
        если мы так оставим, то пользователь может ввести любой тип, который вызовет исключение в 41 строчке;
        и 39 строчка не спасет положение, так как в ней мы не проводит валидацию, а перезаписываем глобальную 
        переменную в локальную область видимости;
    Можно либо аннотацию использовать, но это только разработчикам с idle поможет при разработке;
    Либо проверять тип и вызывать исключение сразу, или переписать метод, 
    чтобы внутри создавать и записывать объект типа Record
    """
    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            # вместо двух методов можно использовать один, если подключить модуль date
            if Record.date == dt.datetime.now().date():
                # можно использовать оператор +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        # аналогично описанному в 40 строке
        today = dt.datetime.now().date()
        for record in self.records:
            # можно обойтись без and, если выписать последовательно операторы сравнения
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # можно вынести вычисление разности в отдельный метод для исключение повторяемости кода (81 строка)
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # для удобства других разработчиков можно использовать Enum для определения списков состояний
    # внутри класса уже указаны курсы валют, можно не указывать их в определении метода
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # не понятно, зачем нужно это переименование, если дело в регистре, то Enum опять же поможет в типизации
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # эту конструкцию можно заменить на словарь и уместить девять строк в одну, что повысит читаемость кода
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # переменная перезаписывается неправильным значением
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # можно вынести вывод строки с количеством валюты в отдельный метод для исключение повторяемости кода
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # если не определять метод дочернего класса, то при вызове метода будет вызываться первый определенный метод
    # по схеме mro
    def get_week_stats(self):
        super().get_week_stats()
