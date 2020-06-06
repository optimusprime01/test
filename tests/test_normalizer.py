from datetime import datetime
from expense_lib.normalizer import normalizer_map
from expense_lib.normalizer import get_expense_type

def test_amex():
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
    assert get_expense_type(list(test_data.keys())) == "amex"
    normalized_data = normalizer_map.get("amex")(test_data)
    assert normalized_data["amount"] == 117.36
    assert normalized_data["is_credit"] is True
    assert normalized_data["description"] == "ONLINE PAYMENT - THANK YOU"
    assert normalized_data["ref_num"] == "320200090698686232"

    test_data["Amount"] = "35.00"
    normalized_data = normalizer_map.get("amex")(test_data)
    assert normalized_data["is_credit"] is False

def test_amex_ytd():
    test_data = {
        "Date": "1/9/20",
        "Description": "ONLINE PAYMENT - THANK YOU",
        "Card Member": "ACHIN S SAGADEVA",
        "Account #": "-220146",
        "Amount": "-117.36",
    }
    assert get_expense_type(list(test_data.keys())) == "amex_ytd"
    normalized_data = normalizer_map.get("amex_ytd")(test_data)
    assert normalized_data["amount"] == 117.36
    assert normalized_data["is_credit"] is True
    assert normalized_data["description"] == "ONLINE PAYMENT - THANK YOU"

    test_data["Amount"] = "35.00"
    normalized_data = normalizer_map.get("amex")(test_data)
    assert normalized_data["is_credit"] is False


def test_bofa():
    test_data = {
        "Posted Date": "12/16/2019",
        "Reference Number": "35006005720001509041659",
        "Payee": "Online payment from CHK 4119",
        "Address": "",
        "Amount": "473.93",
    }
    assert get_expense_type(list(test_data.keys())) == "bofa"
    normalized_data = normalizer_map.get("bofa")(test_data)
    assert normalized_data["amount"] == 473.93
    assert normalized_data["is_credit"] is True
    assert normalized_data["description"] == "Online payment from CHK 4119"
    assert normalized_data["ref_num"] == "35006005720001509041659"

    test_data["Address"] = "AIRBNB.COM    CA"
    test_data["Amount"] = "-159.51"
    normalized_data = normalizer_map.get("bofa")(test_data)
    assert normalized_data["is_credit"] is False
    assert normalized_data["address"] == "AIRBNB.COM    CA"


def test_discover():
    test_data = {
        "Trans. Date": "12/16/2019",
        "Post Date": "12/17/2019",
        "Description": "Online payment from CHK 4119",
        "Amount": "473.93",
        "Category": "ThemePark",
    }
    assert get_expense_type(list(test_data.keys())) == "discover"
    normalized_data = normalizer_map.get("discover")(test_data)
    assert normalized_data["amount"] == 473.93
    assert normalized_data["is_credit"] is False
    assert normalized_data["description"] == "Online payment from CHK 4119"
    assert normalized_data["category"] == "ThemePark"

    test_data["Amount"] = "-400.00"
    normalized_data = normalizer_map.get("discover")(test_data)
    assert normalized_data["is_credit"] is True
