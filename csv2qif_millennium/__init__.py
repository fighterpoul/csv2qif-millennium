import csv
from csv2qif.core import Transaction
import datetime

__mapping = {
    'date': 1,
    'price': 7,
    'recipient': 5,
    'desc': 6,
}


class dialect(csv.Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


def row_converter(csv_row) -> Transaction:
    recipient_ = csv_row[__mapping['recipient']]
    desc_ = csv_row[__mapping['desc']]
    return Transaction(
        date=__get_date(csv_row),
        price=__get_price(csv_row),
        recipient=recipient_ if recipient_ else desc_,
        desc=desc_
    )


def row_filter(csv_row) -> bool:
    try:
        __get_price(csv_row)
        __get_date(csv_row)
    except (IndexError, ValueError):
        return False
    else:
        return True


def __get_price(csv_row) -> float:
    price = csv_row[__mapping['price']]
    if not price:
        price_income_index = __mapping['price'] + 1
        price = csv_row[price_income_index]
    return float(price)


def __get_date(csv_row) -> datetime.datetime:
    return datetime.datetime.strptime(csv_row[__mapping['date']], '%Y-%m-%d')
