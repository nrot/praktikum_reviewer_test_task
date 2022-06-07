import datetime as dt


### Не хватает документирования во всем коде.
### Всего 2 места имеют документирование и то не по формату.


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date()
            if not date  # Не стоит отделять not от условия - плохо читается.
            else dt.datetime.strptime(date, '%d.%m.%Y').date()
        )
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # Эта функция и функция get_week_stats имеют общую логику - нужно взять сумму за период.
        # Для уменьшения количества повторяемого кода, можно написать более общую функцию и вызвает ее с разными аргументами.
        # Например функция get_stats_by_days может принимать за сколько дней брать сумму, а тут ее вызывать с аргументом 0.

        today_stats = 0.0  # Лучше использовать float. Нет гарантий того что у вас будут целые числа.
        today = dt.datetime.now().date() # Лучше заранее узнать текущую дату, что бы при каждой итерации цикла не делать лишнего.
        for record in self.records: # Присваивание переменным имена классов, функций или модулей может привести к ошибке.
            if record.date == today: # Тут могла быть ошибка с тем что пока мы движемся по циклу дата уже сменилась, тогда сумма будет не правильной.
                today_stats += record.amount  # Дальше по коду Вы используете именно такой оператор.
        return today_stats

    def get_week_stats(self):
        # А здесь общую функцию get_stats_by_days вызывать с аргументом 7.
        week_stats = 0.0
        today = dt.datetime.now().date()
        for record in self.records:
            if (today - record.date).days < 7 and (
                today - record.date
            ).days >= 0:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Возвращает остаток калорий на сегодня."""  # Если функция что-то получает, то должен у нее должен быть соответвующий аргумент.
        # В данном случае функция возвращает вызываемому коду значение.
        # Коментарии лучше использовать в формате документации. Правила оформления можно прочитать например тут: https://pythonchik.ru/osnovy/dokumentirovanie-koda-v-python#docstring
        remain = self.limit - self.get_today_stats() # Имена переменных должны нести смысл. Нельзя использовать однобуквенные имена.
        if remain > 0.0:
            return (
                f'Сегодня можно съесть что-нибудь'
                f' ещё, но с общей калорийностью не более {remain} кКал'
            )
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор валют

    Attributes:
        USD_RATE Курс доллар США.
        EURO_RATE Курс Евро.
    """  # Соблюдайте формат документорования.

    USD_RATE = 60.0  # Для того что бы тип был float достачно написать .0
    EURO_RATE = 70.0

    # TIPS: Я не уверен знают ли они уже словари. Но я бы написал что-то типа такого:
    # CURRENCY_MAP = {'usd': {'amount': 60.0, 'name': 'USD'}, 'eur': {'amount': 70.0, 'name': 'Euro', 'rub': {'amount':1.0, 'name':'руб'}
    # Вообще класс валюты был бы лучше.
    # rate = self.CURRENCY_MAP.get(currency)
    # if rate is None:
    #   return f'Ошибка - я не знаю такую валюту: {currency}'
    # else:
    #    cash_remained /= rate['amount']
    #    currency_type = rate['name']
    # ....
    def get_today_cash_remained(
        self,
        currency,  # Работать с курсами валют лучше в разрезе даты и времени. Пока это не требуется в задании.
    ):
        currency_type = ''  #
        currency = currency.lower()  # При сравнении строк необходимо заранее продумать нужно ли учитывать регистр.
        # В данном случае у вас прописные буквы и строчные не важны, так что стоит все привести к прописным буквам.

        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= self.USD_RATE # Поля класса можно получать напрямую из self
            currency_type = 'USD'
        elif currency == 'eur':  # Тут нужно сравнивать с исходной валютой.
            cash_remained /= self.EURO_RATE  # Поля класса можно получать напрямую из self
            currency_type = 'Euro'
        elif currency == 'rub':
            # cash_remained == 1.00 #Оператор == просто сравнит переменную и константу 1.
            # Тут можно написать только тип валюты.
            currency_type = 'руб'
        else:  # Не оставляется if без else. Всегда предусматривайте возможность того что значения могут не совпасть.
            return f'Ошибка - я не знаю такую валюту: {currency}'

        # Можно использовать пустые строки для отделения логических блоков.
        if cash_remained > 0.0:  # Сравнивать лучше с float поскольку выше get_today_stats возвращает теперь float
            return (
                f'На сегодня осталось {cash_remained:.2f} ' #Писать стоит в одном стиле
                f'{currency_type}'
            )
        elif cash_remained == 0.0:
            return 'Денег нет, держись'
        elif cash_remained < 0.0:
            return (
                'Денег нет, держись:'
                f' твой долг - {cash_remained:.2f} {currency_type}'  # Писать стоит в одном стиле.
            )

    # Этот код не нужен поскольку Класс и так унаследует этот метод.
    # Так как логику этого метода вы не меняете, то и лишнего писать нет необходимости.
    # def get_week_stats(self):
        # super().get_week_stats()
