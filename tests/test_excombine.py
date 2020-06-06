from datetime import datetime
from expense_lib.expense import Expense


def test_Expense_basic():

    test_data = {
        "date": datetime.strptime("1/9/20", "%m/%d/%y"),
        "ref_num": "320200090698686232",
        "description": "ONLINE PAYMENT - THANK YOU",
        "amount": 1136.09,
        "category": "test",
        "is_credit": True
    }
    expense1 = Expense.from_dict(test_data)
    assert expense1.date == "01/09/2020"
    assert expense1.amount == 1136.09
    assert expense1.iscredit is True
    assert expense1.expense_category == "test"

    test_data["amount"] = 10000.01
    expense3 = Expense.from_dict(test_data)
    assert expense3 == expense1

    test_data["date"] = datetime.strptime("1/9/19", "%m/%d/%y")
    expense4 = Expense.from_dict(test_data)
    assert expense4 < expense3

    test_data["date"] = datetime.strptime("10/29/21", "%m/%d/%y")
    expense5 = Expense.from_dict(test_data)
    assert expense5 > expense3
    assert expense5 > expense4
