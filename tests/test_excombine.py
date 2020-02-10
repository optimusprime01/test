import sys

sys.path.append("..")
from excombine import Expense


def test_Expense_basic():

    test_data = {
        "Date": "1/9/20",
        "Reference": "320200090698686232",
        "Description": "ONLINE PAYMENT - THANK YOU",
        "Card Member": "ACHIN S SAGADEVA",
        "Card Number": "-22006",
        "Amount": "-117.36",
        "Category": "",
        "Type": "CREDIT",
    }
    expense1 = Expense.from_dict(test_data, expense_type="amex")
    assert expense1.date == "01/09/2020"
    assert expense1.amount == 117.36
    assert expense1.iscredit is True

    test_data = {
        "Date": "1/5/20",
        "Reference": "320200050631427035",
        "Description": "ZIPCAR.COM          BOSTON              MA",
        "Card Member": "SHWINI SENTHIL KUMARAN",
        "Card Number": "-22014",
        "Amount": "35.00",
        "Category": "Transportation-Auto Services",
        "Type": "DEBIT",
    }
    expense2 = Expense.from_dict(test_data, expense_type="amex")
    assert expense2.date == "01/05/2020"
    assert expense2.amount == 35.00
    assert expense2.iscredit is False

    test_data = {
        "Posted Date": "12/16/2019",
        "Reference Number": "35006005720001509041659",
        "Payee": "Online payment from CHK 4119",
        "Address": "",
        "Amount": "473.93",
    }
    expense3 = Expense.from_dict(test_data, expense_type="bofa")
    assert expense3.date == "12/16/2019"
    assert expense3.amount == 473.93
    assert expense3.iscredit is True

    test_data = {
        "Posted Date": "11/23/2019",
        "Reference Number": "24231689327200848172642",
        "Payee": "OIRBNB HMAQPWR5E8 AIRBNB.",
        "Address": "AIRBNB.COM    CA",
        "Amount": "-159.51",
    }
    expense4 = Expense.from_dict(test_data, expense_type="bofa")
    assert expense4.date == "11/23/2019"
    assert expense4.amount == 159.51
    assert expense4.iscredit is False

    test_data = {
        "Date": "11/23/19",
        "Reference": "3202000906986234234236232",
        "Description": "ONLINE SPENT - THANK YOU",
        "Card Member": "ACHIN SAGADEVA",
        "Card Number": "-22006",
        "Amount": "103.36",
        "Category": "",
        "Type": "DEBIT",
    }
    expense5 = Expense.from_dict(test_data, expense_type="amex")
    assert expense5.date == "11/23/2019"
    assert expense5.amount == 103.36
    assert expense5.iscredit is False

    assert expense4 < expense3
    assert expense5 == expense4
    assert expense1 > expense2
